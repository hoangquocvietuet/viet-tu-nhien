#!/usr/bin/env python3
"""Retrieve native-Vietnamese references for a draft (skill viet-tu-nhien). sqlite3 FTS5 + sqlite-vec.

  python3 rag/viet_rag.py search "<text>" [--kind pair,user_flag] [-k 5] [--mode keyword|vector|hybrid]
  python3 rag/viet_rag.py ref <draft.md|-> [--register narration|chat|doc] [--per-sentence 3] [--max-chars 6000]
  python3 rag/viet_rag.py --selftest [--mode …]

`ref` splits the draft into sentences and, per sentence, prints a few references: scanner hits first
(scripts/viet_scan.py pattern row + its closest real pair), then user-flagged lines, pairs, names
for big ideas (cách gọi), connectives, native excerpts. Items already shown for an earlier sentence
are not repeated. The index (rag/viet.db) is rebuilt automatically when a source file is newer.

Retrieval modes: `keyword` (FTS5 bm25 over syllables and syllable bigrams), `vector` (cosine over
gte-multilingual-base embeddings in rag/viet_vec.db, see rag/vec.py), `hybrid` (reciprocal rank fusion
of both). Default: hybrid when the model and vector DB are there, else keyword, said in the output.
"""
import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

sys.dont_write_bytecode = True
RAG = Path(__file__).resolve().parent
sys.path[:0] = [str(RAG), str(RAG.parent / 'scripts')]
import build  # noqa: E402
import viet_scan  # noqa: E402
import vec  # noqa: E402

STOP = set('là của và thì mà đã được những các một có cho với này ấy đó ở trong không cũng vẫn lại rồi nên '
           'như khi để từ thế nó họ ta tôi mình bạn'.split())
TIER = {'user_flag': 1, 'pair': 2, 'pattern': 2, 'overcorrection': 2, 'keep': 2,
        'naming': 3, 'avoid': 3, 'connective': 4, 'excerpt': 5}
FITS = {'narration': {'', 'narration', 'memoir', 'formal'}, 'chat': {'', 'chat'}, 'doc': {'', 'doc', 'formal'}}
WEIGHTS = (1.0, 2.5, 0.25)  # bm25 weights for columns t (text), g (syllable bigrams), x (notes, English)
MODES = ('keyword', 'vector', 'hybrid')
RRF_K = 10  # reciprocal rank fusion: score = Σ 1000 / (RRF_K + rank); 10 beat 3/5/15/20/30/60 on the selftest
SIM_BAND = 0.05  # a unit with no shared content bigram stays if its similarity is within this of the best


def connect():
    if build.stale():
        build.build()
    con = sqlite3.connect(build.DB)
    con.row_factory = sqlite3.Row
    return con


class Retrieval:
    """Mode in use, the vector DB connection (None in keyword mode) and a one-line note for headers."""

    def __init__(self, mode=None):
        why = '' if mode == 'keyword' else vec.unavailable()
        if why and mode:
            sys.exit(f'--mode {mode}: vector layer unavailable: {why}')
        self.mode = 'keyword' if why else mode or 'hybrid'
        self.vcon = None if self.mode == 'keyword' else vec.connect()
        self.note = (f'keyword only (vector layer off: {why})' if why else
                     'keyword' if self.mode == 'keyword' else f'{self.mode} ({vec.NAME})')

    def embed(self, texts):
        return list(vec.embed(texts)) if self.vcon else [None] * len(texts)


# ---------- query ----------

def terms(text):
    syl = [s for s in build.syllables(text) if not s.isdigit()]
    pairs = [f'{a}_{b}' for a, b in zip(syl, syl[1:]) if not (a in STOP and b in STOP)]
    singles = [s for s in dict.fromkeys(syl) if s not in STOP]
    return list(dict.fromkeys(pairs)), singles


def fts_query(gram_terms, singles):
    q = [f'g:"{g}"' for g in gram_terms] + [f'{{t x}}:"{s}"' for s in singles]
    return ' OR '.join(q)


def keyword_hits(con, text, kinds, limit):
    """FTS candidates, best bm25 first."""
    gram_terms, singles = terms(text)
    if not gram_terms and not singles:
        return []
    sql = ('SELECT u.*, -bm25(fts, ?, ?, ?) AS score FROM fts JOIN units u ON u.id = fts.rowid '
           'WHERE fts MATCH ?')
    args = [*WEIGHTS, fts_query(gram_terms, singles)]
    if kinds:
        sql += f' AND u.kind IN ({",".join("?" * len(kinds))})'
        args += list(kinds)
    sql += ' ORDER BY bm25(fts, ?, ?, ?) LIMIT ?'
    args += [*WEIGHTS, limit]
    return [dict(r) for r in con.execute(sql, args)]


def vector_hits(con, vcon, qvec, kinds, limit):
    """Nearest units by cosine similarity (`sim`), best first; score = 100 × sim."""
    near = vec.knn(vcon, qvec, limit * 8 if kinds else limit)
    rows = {r['uid']: dict(r) for r in con.execute(
        f'SELECT * FROM units WHERE uid IN ({",".join("?" * len(near))})', [u for u, _ in near])}
    out = []
    for uid, sim in near:
        h = rows.get(uid)
        if h and (not kinds or h['kind'] in kinds):
            out.append(dict(h, sim=sim, score=100 * sim))
    return out[:limit]


def search(con, text, kinds=None, limit=40, register=None, rt=None, qvec=None):
    """Candidates with score and syllable/bigram overlap, best first.

    keyword: score = bm25. vector: score = 100 × cosine. hybrid: reciprocal rank fusion, score =
    Σ 1000 / (RRF_K + rank) over the keyword and vector lists, so a unit near the top of both wins.
    Register mismatch: score × 0.7."""
    gram_terms, singles = terms(text)
    if not gram_terms and not singles:
        return []
    mode = rt.mode if rt else 'keyword'
    kw = keyword_hits(con, text, kinds, limit) if mode != 'vector' else []
    vh = []
    if mode != 'keyword':
        vh = vector_hits(con, rt.vcon, rt.embed([text])[0] if qvec is None else qvec, kinds, limit)
    qg, qs = set(gram_terms), set(singles)
    for h in kw + vh:
        if h['text'] is None:  # build.py stores text only when it differs from t
            h['text'] = build.clean(h['t'])
        shared = qg & set(build.grams(h['t']).split())
        h['grams'] = len(shared)
        h['content'] = sum(1 for g in shared if not STOP & set(g.split('_')))
        h['singles'] = len(qs & set(build.syllables(h['t'])))
        if register and h['register'] not in FITS.get(register, {''}):
            h['score'] *= 0.7
    for h in kw:
        h['bm25'] = h['score']
    kw.sort(key=lambda h: -h['score'])
    vh.sort(key=lambda h: -h['score'])
    if mode != 'hybrid':
        return kw or vh
    fused = {}
    for hits in (kw, vh):
        for rank, h in enumerate(hits, 1):
            f = fused.setdefault(h['uid'], dict(h, score=0.0))
            f.update({k: h[k] for k in ('sim', 'bm25') if k in h})
            f['score'] += 1000 / (RRF_K + rank)
    return sorted(fused.values(), key=lambda h: -h['score'])


def near_best(hits, band=SIM_BAND):
    """Predicate: the unit's vector similarity is within `band` of the best one (always False in keyword mode)."""
    top = max((h.get('sim', 0) for h in hits), default=0)
    return lambda h: 'sim' in h and h['sim'] >= top - band


def relevant(hits, floor=0.35):
    """Drop hits far below the best one, or matching only scattered single syllables and not close in meaning."""
    if not hits:
        return []
    best, near = hits[0]['score'], near_best(hits)
    return [h for h in hits if h['score'] >= floor * best and (h['content'] >= 1 or h['singles'] >= 4 or near(h))]


def prioritise(hits):
    """Strong hits in kind order (user_flag, pair, naming, connective, excerpt), then the rest by score.

    Strong = two content bigrams shared with the sentence, or one plus a bm25 near the best, or a vector
    similarity close to the best one."""
    if not hits:
        return []
    best, near = max(h.get('bm25', 0) for h in hits), near_best(hits, SIM_BAND / 2)

    def strong(h):
        return h['content'] >= 2 or (h['content'] >= 1 and h.get('bm25', 0) >= 0.6 * best) or near(h)
    return sorted(hits, key=lambda h: (TIER[h['kind']] if strong(h) else 9, -h['score']))


def scanner_ids(findings):
    return list(dict.fromkeys(f['id'].rstrip('n') for f in findings))


def best_pair(con, pid, text):
    """Pattern row of `pid` plus the pair of that pattern closest to `text`."""
    pat = con.execute("SELECT * FROM units WHERE uid = ?", (f'pat:{pid}',)).fetchone()
    rows = con.execute("SELECT * FROM units WHERE kind = 'pair' AND ' ' || pids || ' ' LIKE ?",
                       (f'% {pid} %',)).fetchall()
    qg, qs = terms(text)
    qg, qs = set(qg), set(qs)

    def fit(r):
        return 3 * len(qg & set(build.grams(r['t']).split())) + len(qs & set(build.syllables(r['t'])))
    pair = max(rows, key=fit, default=None) if rows else None
    return (dict(pat) if pat else None), (dict(pair) if pair else None)


# ---------- rendering ----------

def cut(s, n):
    s = ' '.join((s or '').split())
    return s if len(s) <= n else s[:n - 1].rstrip() + '…'


def short_src(src):
    """`references/pairs.md#e:184` → `pairs.md:184` for tight packs."""
    path, _, rest = src.partition('#')
    line = rest.rsplit(':', 1)[-1] if rest else path.rsplit(':', 1)[-1]
    return f"{path.rsplit('/', 1)[-1].split(':')[0]}:{line}"


def item_parts(h, side=400):
    """(main line, detail, source pointer) of one unit; each side of a pair is cut to `side` chars."""
    k, src = h['kind'], h.get('src', '')

    def fix(bad, nat):
        """Both sides cut to `side`; long pairs start a little before the first changed word."""
        start = 0
        if len(bad) > side or len(nat) > side:
            same = len(os.path.commonprefix([bad, nat]))
            start = bad.rfind(' ', 0, max(0, same - side // 3)) + 1
        lead = '…' if start else ''
        right = cut(lead + nat[start:], side) if nat else '(no fix given)'
        return f"`{cut(lead + bad[start:], side)}` → `{right}`"
    if k == 'scan':
        pat, pair = h['pattern'], h['pair']
        best = pair or pat
        name = f" {pat['text']}" if pat else ''
        return (f"**scan {h['pid']}**{name}: {fix(best['bad'], best['natural'])}",
                pat['note'] if pat else pair['note'], best['src'])
    if k == 'user_flag':
        return f"**{h['uid']} user rejected** `{h['bad']}`", f"user: {h['note']}", src
    if k in ('pair', 'overcorrection', 'pattern'):
        tag = {'pair': f"pair {h['pid']}".strip(), 'overcorrection': 'over-fix', 'pattern': f"pattern {h['pid']}"}[k]
        return f"**{tag}** {fix(h['bad'], h['natural'])}", h['note'] or h['text'], src
    if k == 'keep':
        return f"**keep as is** `{h['text']}` {h['note']}", '', src
    if k == 'naming':
        concept = json.loads(h['extra']).get('concept', '')
        return f"**cách gọi** {concept} → {h['text']}", h['note'], src
    if k == 'connective':
        body = ' — '.join(p for p in (h['note'], h['natural']) if p)
        return f"**nối** {h['text']}" + (f": {body}" if body else ''), '', src
    if k == 'avoid':
        return f"**sáo, tránh** {h['text']}", h['note'], src
    return f"**{h['uid']}** `{h['text']}`", h['note'], src


def item_lines(h, cap, two=True, short=False):
    """One or two Markdown lines for a unit, at most `cap` chars each, ending with the source pointer."""
    src = item_parts(h)[2]
    src = short_src(src) if short else src
    room = cap if two else cap - len(src) - 3
    main, sub, _ = item_parts(h, side=max(24, (room - 40) // 2))
    if two and sub:
        return [cut('- ' + main, cap), '  ↳ ' + cut(f'{sub} · {src}', cap)]
    return [cut('- ' + main, room) + f' · {src}']


def split_sentences(text):
    """(start, end) spans of sentences in one paragraph."""
    spans, start = [], 0
    for m in re.finditer(r'(?<=[.!?…])["”’)]*\s+|\n+', text):
        if text[start:m.start()].strip():
            spans.append((start, m.start()))
        start = m.end()
    if text[start:].strip():
        spans.append((start, len(text)))
    return spans


def clean_draft(text):
    out, fence = [], False
    for line in build.nfc(text).split('\n'):
        if line.strip().startswith('```'):
            fence = not fence
            continue
        if fence or line.lstrip().startswith('#'):
            out.append('')
            continue
        out.append(re.sub(r'^\s*(?:[-*>]|\d+\.)\s+', '', line))
    return '\n'.join(out)


def collect(con, text, register, depth=8, rt=None):
    """Per sentence: (sentence, scanner items, ranked hits). Dedupe happens in render()."""
    sents = []
    for _, _, para in viet_scan.units_from_text(clean_draft(text)):
        findings = viet_scan.scan_text(para, register)
        for a, z in split_sentences(para):
            sent = para[a:z].strip()
            if len(build.syllables(sent)) < 2:
                continue
            scans = []
            for pid in scanner_ids([f for f in findings if a <= f['start'] < z]):
                pat, pair = best_pair(con, pid, sent)
                if pat or pair:
                    scans.append({'kind': 'scan', 'uid': f'pat:{pid}', 'pid': pid, 'pattern': pat, 'pair': pair})
            sents.append((sent, scans))
    qvecs = rt.embed([s for s, _ in sents]) if rt else [None] * len(sents)  # one batch for the whole draft
    out = []
    for (sent, scans), qvec in zip(sents, qvecs):
        hits = relevant(search(con, sent, register=register, rt=rt, qvec=qvec))
        top_bm25 = max((h.get('bm25', 0) for h in hits), default=0) or 1
        for h in hits:
            h['rel'] = h['score'] / hits[0]['score']
            # home key in render(): a unit sharing wording goes where its bm25 is nearest that sentence's best
            h['home'] = (True, h['bm25'] / top_bm25) if h['content'] >= 1 and 'bm25' in h else (False, h['rel'])
        hits = prioritise(hits)[:depth]
        out.append((sent, scans, hits))
    return out


def render(rows, register, cap, per, sent_cap, two, short, note='keyword'):
    lines = [f'# Reference pack · {len(rows)} sentences · register {register} · retrieval {note}',
             'Scanner hits are cues to reread, not verdicts; copy the joins and names, never the facts.']
    home = {}  # uid → sentence where it shares wording best, else where it matches best (see collect())
    for i, (_, _, hits) in enumerate(rows):
        for h in hits:
            if h['home'] > home.get(h['uid'], (-1, (False, 0)))[1]:
                home[h['uid']] = (i, h['home'])
    seen = set()
    for i, (sent, scans, hits) in enumerate(rows, 1):
        items, again = [], []
        for s in scans:
            if s['uid'] in seen:
                again.append(s['pid'])
            elif len(items) < per:
                items.append(s)
                seen.update({s['uid'], s['pair']['uid'] if s['pair'] else ''})
        for h in hits:
            if len(items) >= per:
                break
            if h['uid'] not in seen and home[h['uid']][0] == i - 1:
                items.append(h)
                seen.add(h['uid'])
        head = f'\n**{i}.** {cut(sent, sent_cap)}'
        if again:
            head += f" _(also {', '.join(again)} ↑)_"
        lines.append(head if items or again else head + ' _(no match)_')
        for h in items:
            lines += item_lines(h, cap, two, short)
    return '\n'.join(lines)


BUDGET = (  # (chars per line, items per sentence cap, chars of the draft sentence, two-line items, short pointers)
    (240, 3, 400, True, False), (180, 3, 240, True, False), (160, 3, 200, True, True), (150, 3, 160, False, True),
    (130, 2, 140, False, True), (110, 2, 110, False, True), (100, 1, 100, False, True), (80, 1, 70, False, True))


def pack(con, text, register='narration', per=3, max_chars=6000, rt=None):
    """Reference pack, tightened step by step (shorter lines, fewer items) until it fits max_chars."""
    rows = collect(con, text, register, rt=rt)
    note = rt.note if rt else 'keyword'
    for cap, n, sent_cap, two, short in BUDGET:
        out = render(rows, register, cap, min(per, n), sent_cap, two, short, note)
        if len(out) <= max_chars:
            return out
    return out[:max_chars - 40].rsplit('\n', 1)[0] + '\n… (pack cut at --max-chars)'


# ---------- CLI ----------

SELFTEST = [
    ('nhận về một câu thủ tục', {'U08', 'pat:A14'}),
    ('Còn làm sao cho một thuộc địa thoát ra thì chưa nơi nào chỉ cho.', {'pair:cg.applied.1', 'U12'}),
    ('Phản biện khiến mình sửa những chỗ này so với bản đầu', {'U01', 'pair:E02.2'}),
    ('Caffeine được hấp thụ một cách nhanh chóng', {'pat:B03', 'pair:B03.1'}),
    ('đang lưỡng lự chưa biết ngã về đâu', {'loi-binh:TD06', 'name:cg.12', 'name:loi-binh.17'}),
    ('Thư đi chừng một tháng thì có hồi âm', {'conn:19'}),
    ('rốt cuộc cái gì giữ được một kinh đô', {'pat:A01', 'pair:A01.1', 'pair:A01.2'}),
    ('nên triều đại chẳng được lâu bền', {'keep:7'}),
    ('Mục tiêu giữ nguyên, còn cách đi thì mỗi tập một kiểu', {'U04', 'pair:g.1'}),
    ('kéo xe chạy suốt ngày mà ăn không đủ', {'but-ky:TK10', 'name:but-ky.1', 'name:but-ky.2', 'name:cg.19'}),
    ('một mốc son chói lọi của dân tộc', {'avoid:loi-binh.2', 'avoid:cg.2'}),
]

# Draft sentences with no content bigram in common with their target: keyword mode misses all eight
# (measured 2026-10-27). Hybrid must keep at least SEMANTIC_MIN of them.
SEMANTIC = [
    ('Người muốn tìm cách giải phóng đất nước khỏi ách ngoại bang',
     {'name:cg.3', 'name:cg.11', 'name:sach-su.10', 'pair:cg.applied.1', 'pair:cg.applied.2'}),
    ('Đơn xin nhập học bị bác bằng một lý do giấy tờ khô khốc',
     {'U08', 'U09', 'pat:A14', 'pair:A12.7', 'pair:cg.applied.3'}),
    ('Cuộc sống cơ cực, làm quần quật cả ngày mà vẫn đói',
     {'name:cg.19', 'name:cg.20', 'name:but-ky.2', 'name:sach-su.18', 'but-ky:TK10'}),
    ('Người mong ngày hồi hương', {'name:cg.22', 'but-ky:CB32'}),
    ('Người lên bờ ở xứ sở của người Pháp', {'name:cg.17', 'name:sach-su.16'}),
    ('Người quen thêm mấy bạn chung lý tưởng', {'name:cg.26'}),
    ('Sau biến cố đó, đời Người đổi khác', {'name:cg.23'}),
    ('Mọi lối thử qua đều dẫn tới chỗ không lối ra', {'name:cg.12', 'name:cg.13', 'name:cg.15', 'pair:cg.applied.2'}),
]
SEMANTIC_MIN = 7


def run_cases(con, cases, rt):
    ok = 0
    for q, want in cases:
        top = [h['uid'] for h in search(con, q, rt=rt)[:3]]
        hit = bool(want & set(top))
        ok += hit
        print(f"{'ok ' if hit else 'MISS'} {cut(q, 48):48} top3={top} want={sorted(want)}")
    return ok


def selftest(con, mode=None):
    """hit@3 of SELFTEST (wording) and SEMANTIC (meaning) per mode. Pass: every SELFTEST case in keyword and
    hybrid, at least SEMANTIC_MIN SEMANTIC cases in hybrid (modes not run are skipped)."""
    modes = [mode] if mode else ['keyword'] + ([] if vec.unavailable() else ['vector', 'hybrid'])
    if not mode and len(modes) == 1:
        print(f'vector layer off: {vec.unavailable()}')
    summary, passed = [], True
    for m in modes:
        rt = Retrieval(m)
        print(f'## mode {rt.note}')
        a, b = run_cases(con, SELFTEST, rt), run_cases(con, SEMANTIC, rt)
        summary.append(f'{m:8} hit@3 = {a}/{len(SELFTEST)} · meaning-only {b}/{len(SEMANTIC)}')
        passed &= (m == 'vector' or a == len(SELFTEST)) and (m != 'hybrid' or b >= SEMANTIC_MIN)
    print('\n'.join(summary))
    return passed


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode_help = 'retrieval mode; default hybrid when the vector layer is available, else keyword'
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--mode', choices=MODES, help=mode_help)
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('search', help='ranked hits for a phrase or sentence')
    s.add_argument('text')
    s.add_argument('--kind', help='comma list: ' + ','.join(TIER))
    s.add_argument('-k', type=int, default=5)
    s.add_argument('--register', choices=list(FITS))
    r = sub.add_parser('ref', help='reference pack for a draft')
    r.add_argument('draft', help='Markdown/text file, or - for stdin')
    r.add_argument('--register', choices=list(FITS), default='narration')
    r.add_argument('--per-sentence', type=int, default=3)
    r.add_argument('--max-chars', type=int, default=6000)
    for p in (s, r):
        p.add_argument('--mode', choices=MODES, default=argparse.SUPPRESS, help=mode_help)
    args = ap.parse_args()
    con = connect()
    if args.selftest:
        sys.exit(0 if selftest(con, args.mode) else 1)
    if args.cmd == 'search':
        rt = Retrieval(args.mode)
        kinds = [k.strip() for k in args.kind.split(',')] if args.kind else None
        for i, h in enumerate(search(con, args.text, kinds, register=args.register, rt=rt)[:args.k], 1):
            sim = f" sim={h['sim']:.3f}" if 'sim' in h else ''
            print(f"{i}. [{h['kind']}] {h['uid']}  score={h['score']:.2f} bigrams={h['grams']}{sim}")
            for line in item_lines(h, 240):
                print('   ' + line.lstrip())
        fired = scanner_ids(viet_scan.scan_text(args.text, args.register or 'narration'))
        if fired:
            print('scanner: ' + ', '.join(fired) + ' (patterns.md rows: rag/viet_rag.py search "<id>" --kind pattern)')
        print(f'retrieval: {rt.note}')
    elif args.cmd == 'ref':
        rt = Retrieval(args.mode)
        text = sys.stdin.read() if args.draft == '-' else Path(args.draft).read_text()
        print(pack(con, text, args.register, args.per_sentence, args.max_chars, rt))
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
