#!/usr/bin/env python3
"""Build rag/viet.db, the retrieval index of skill viet-tu-nhien (sqlite3 FTS5), and rag/viet_vec.db (sqlite-vec).

  python3 rag/build.py              rebuild viet.db; refresh viet_vec.db too when the model is downloaded
  python3 rag/build.py --vectors    same, downloading the embedding model first if it is missing
  python3 rag/build.py --stats      rebuild, then print unit counts per kind and the DB sizes

One row per unit: pattern, pair, keep, overcorrection, excerpt, naming, avoid, connective, user_flag.
Every row keeps a source pointer `file#anchor:line`. viet.db is a build artifact; viet_rag.py
rebuilds it when any source file is newer, and refreshes viet_vec.db (rag/vec.py) when viet.db is newer.
New corpus files (`references/corpus/*.md` or `*.jsonl` in the research contract format) are picked
up on the next build.
"""
import argparse
import json
import os
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

RAG = Path(__file__).resolve().parent
SKILL = RAG.parent
DB = RAG / 'viet.db'
REF = SKILL / 'references'
CORPUS = REF / 'corpus'
FLAGS = SKILL / 'evals' / 'user-flagged.md'

PAT_ID = re.compile(r'\b([A-G]\d{2})\b')
URL = re.compile(r'https?://[^\s)\]>|]+')
TICK = re.compile(r'`([^`]+)`')


# ---------- text helpers shared with viet_rag.py ----------

def nfc(s):
    return unicodedata.normalize('NFC', s or '')


def syllables(s):
    """Lower-case syllables, the same split unicode61 makes (letters and digits)."""
    return re.findall(r'[^\W_]+', nfc(s).lower())


def grams(s):
    """Space-joined `a_b` bigrams of each segment (segments split on ' | ')."""
    out = []
    for seg in nfc(s).split(' | '):
        syl = syllables(seg)
        out += [f'{a}_{b}' for a, b in zip(syl, syl[1:])]
    return ' '.join(out)


def slug(heading):
    """GitHub-style anchor of a markdown heading."""
    h = nfc(heading).strip().lower()
    h = re.sub(r'[^\w\- ]', '', h)
    return h.replace(' ', '-')


def clean(s):
    s = nfc(s).replace('**', '').replace('<', '').replace('>', '')
    return re.sub(r'\s+', ' ', s).strip()


def unquote(s):
    s = clean(s)
    if len(s) > 1 and s[0] in '“"' and s[-1] in '”"':
        s = s[1:-1].strip()
    return s


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


class Units:
    def __init__(self):
        self.rows, self.seen = [], {}

    def add(self, kind, uid, src, t, x='', pid='', pids=(), register='', bad='', natural='', text='',
            note='', extra=None):
        n = self.seen.get(uid, 0)
        self.seen[uid] = n + 1
        if n:
            uid = f'{uid}~{n + 1}'
        pids = sorted({p for p in (pid, *pids) if p})
        self.rows.append(dict(uid=uid, kind=kind, pid=pid, pids=' '.join(pids), register=register,
                              bad=clean(bad), natural=clean(natural), text=clean(text), note=clean(note),
                              extra=json.dumps(extra or {}, ensure_ascii=False), src=src,
                              t=nfc(t), x=nfc(x)))


def rel(path):
    return str(path.relative_to(SKILL))


# ---------- references/pairs.md ----------

def split_outside(line, sep=';'):
    """Split on `sep` outside backticks and [brackets]."""
    out, buf, tick, depth = [], [], False, 0
    for ch in line:
        if ch == '`':
            tick = not tick
        elif not tick and ch == '[':
            depth += 1
        elif not tick and ch == ']':
            depth = max(0, depth - 1)
        if ch == sep and not tick and depth == 0:
            out.append(''.join(buf))
            buf = []
        else:
            buf.append(ch)
    out.append(''.join(buf))
    return out


def arrow_at(seg):
    """Index of the first → outside backticks, or -1."""
    tick = False
    for i, ch in enumerate(seg):
        if ch == '`':
            tick = not tick
        elif ch == '→' and not tick:
            return i
    return -1


PAIR_SECTIONS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'eval'}


def parse_pairs(u):
    path = REF / 'pairs.md'
    src0 = rel(path)
    anchor, pid, label, urls = '', '', '', {}
    counter = {}
    last = None
    for ln, raw in enumerate(nfc(path.read_text()).split('\n'), 1):
        line = raw.strip()
        m = re.match(r'<a id="([^"]+)"></a>', line)
        if m:
            anchor, pid, label = m.group(1), '', ''
            continue
        if not anchor or line.startswith('## ') or not line:
            continue
        src = f'{src0}#{anchor}:{ln}'
        reg = 'chat' if anchor == 'g' else 'doc' if anchor == 'eval' else ''
        if anchor in PAIR_SECTIONS:
            m = re.match(r'\*\*([A-G]\d{2})\b[^*]*\*\*\s*(.*)$', line)
            if m:
                pid, line = m.group(1), m.group(2)
                if not line:
                    continue
            lpid = pid  # a bold header id covers the bullets below it; a bullet's own id covers that bullet
            if line.startswith('- '):
                line = line[2:]
                m = re.match(r'([A-G]\d{2})\s+(.*)$', line)
                if m:
                    lpid, line = m.group(1), m.group(2)
            elif not m:
                continue
            if '`' not in line:
                continue
            for seg in split_outside(line):
                ticks = list(TICK.finditer(seg))
                if not ticks:
                    if last is not None:
                        last['note'] = clean(last['note'] + '; ' + seg)
                    continue
                cut = arrow_at(seg)
                if cut >= 0:
                    bad = ' / '.join(t.group(1) for t in ticks if t.start() < cut)
                    nat = ' / '.join(t.group(1) for t in ticks if t.start() > cut)
                else:
                    bad, nat = ' / '.join(t.group(1) for t in ticks), ''
                note = clean(TICK.sub('…', seg).replace('→', ' ').strip(' …/,'))
                key = lpid or anchor
                counter[key] = counter.get(key, 0) + 1
                pids = PAT_ID.findall(note)
                u.add('pair', f'pair:{key}.{counter[key]}', src, t=f'{bad} | {nat}', x=f'{lpid} {note}',
                      pid=lpid, pids=pids, register=reg, bad=bad, natural=nat, note=note)
                last = u.rows[-1]
        elif anchor == 'giữ-nguyên':
            for t in TICK.finditer(line):
                after = line[t.end():].split('`')[0]
                note = clean(re.sub(r'^[\s,(]*|[)\s,.]*$', '', after)) if after.strip(' ,.') else ''
                counter['keep'] = counter.get('keep', 0) + 1
                u.add('keep', f'keep:{counter["keep"]}', src, t=t.group(1), x=note, text=t.group(1), note=note)
        elif anchor == 'sửa-quá-tay':
            m = re.match(r'(\d+)\.\s+(.*)$', line)
            if not m:
                continue
            ticks = [t.group(1) for t in TICK.finditer(m.group(2))]
            note = clean(TICK.sub('…', m.group(2)))
            u.add('overcorrection', f'over:{m.group(1)}', src, t=' | '.join(ticks), x=note,
                  bad=ticks[0] if ticks else '', natural=' / '.join(ticks[1:]), note=note)
        elif anchor == 'mạch-kể':
            for code, url in re.findall(r'\*\*(\w+)\*\* = .*?(https?://\S+?)\s*[;(]', line):
                urls[code] = url
            m = re.match(r'\*\*(.+?)\*\*', line)
            if m and not line.startswith('- '):
                label = clean(m.group(1))
                continue
            if line.startswith('- ') and '`' in line:
                ticks = [t.group(1) for t in TICK.finditer(line)]
                code = (re.findall(r'\[(\w+)\]\s*$', line) or [''])[0]
                counter['mk'] = counter.get('mk', 0) + 1
                u.add('excerpt', f'pairs-mk:{counter["mk"]}', src, t=' | '.join(ticks), x=label,
                      register='memoir', text=' '.join(ticks), note=label,
                      extra={'source': code, 'url': urls.get(code, '')})


# ---------- references/patterns.md ----------

def parse_patterns(u):
    path = REF / 'patterns.md'
    anchor = ''
    for ln, raw in enumerate(nfc(path.read_text()).split('\n'), 1):
        if raw.startswith('## '):
            anchor = slug(raw[3:])
            continue
        m = re.match(r'\|\s*([A-G]\d{2})\s*\|', raw)
        if not m:
            continue
        c = cells(raw)
        if len(c) < 8:
            continue
        pid, name, eng, bad, nat, why, detect, source = c[:8]
        u.add('pattern', f'pat:{pid}', f'{rel(path)}#{anchor}:{ln}', t=f'{bad} | {nat} | {name}',
              x=f'{pid} {eng} {why}', pid=pid, register='chat' if pid[0] == 'G' else '',
              bad=bad, natural=nat, text=name, note=why,
              extra={'english': clean(eng), 'detect': clean(detect), 'source': clean(source)})


# ---------- references/cach-goi.md ----------

def parse_cach_goi(u):
    path = REF / 'cach-goi.md'
    anchor, mode, n = '', '', {}
    for ln, raw in enumerate(nfc(path.read_text()).split('\n'), 1):
        if raw.startswith('## '):
            anchor = slug(raw[3:])
            mode = 'applied' if raw.startswith('## Applied') else 'avoid' if raw.startswith('## Sáo') else 'naming'
            continue
        src = f'{rel(path)}#{anchor}:{ln}'
        if mode == 'avoid' and raw.strip():
            body = raw.split(':', 1)[1] if ':' in raw.split('(')[0] else raw
            body = body.split('. Quote them')[0]
            for seg in split_outside(body):
                seg = clean(seg).rstrip('.')
                if seg:
                    n['avoid'] = n.get('avoid', 0) + 1
                    u.add('avoid', f'avoid:cg.{n["avoid"]}', src, t=seg, text=seg,
                          note='praise/verdict: quote, do not narrate in it')
            continue
        if not raw.startswith('|') or re.match(r'\|\s*-', raw):
            continue
        c = cells(raw)
        if len(c) < 3 or c[0] in ('ý trong đầu', 'rejected'):
            continue
        if mode == 'applied':
            n['applied'] = n.get('applied', 0) + 1
            u.add('pair', f'pair:cg.applied.{n["applied"]}', src, t=f'{c[0]} | {c[2]}', x=c[1],
                  bad=c[0], natural=c[2], note=f'concept: {c[1]}')
        else:
            n['naming'] = n.get('naming', 0) + 1
            u.add('naming', f'name:cg.{n["naming"]}', src, t=f'{c[1]} | {c[2]}', x=c[0],
                  text=c[1], note=c[2], extra={'concept': clean(c[0])})


# ---------- references/connectives.md ----------

def parse_connectives(u):
    path = REF / 'connectives.md'
    anchor, group, head, n = '', '', [], 0
    for ln, raw in enumerate(nfc(path.read_text()).split('\n'), 1):
        src = f'{rel(path)}#{anchor}:{ln}'
        if raw.startswith('## '):
            group, anchor, head = raw[3:].strip(), slug(raw[3:]), []
            continue
        if raw.startswith('Essay-only'):
            words = raw.split(':', 1)[1].strip().rstrip('.')
            u.add('avoid', 'avoid:conn.essay', f'{rel(path)}:{ln}', t=words, x='essay connectives F01',
                  pid='F01', text=words, note='essay-only: not at a sentence start in narration or chat (F01)')
            continue
        if not raw.startswith('|') or re.match(r'\|\s*-', raw):
            continue
        c = cells(raw)
        if c[0] == 'từ':
            head = c
            continue
        row = dict(zip(head, c))
        words, use, ex = row.get('từ', ''), row.get('dùng khi', ''), row.get('ví dụ', '')
        n += 1
        u.add('connective', f'conn:{n}', src, t=f'{words} | {use} | {ex}', x=group, text=words,
              natural=ex, note=use, extra={'group': group})


# ---------- evals/user-flagged.md ----------

def parse_flags(u):
    head, prev = [], ''
    for ln, raw in enumerate(nfc(FLAGS.read_text()).split('\n'), 1):
        if not raw.startswith('|') or re.match(r'\|\s*-', raw):
            continue
        c = cells(raw)
        if c[0] == 'id':
            head = c
            continue
        if not re.match(r'U\d+$', c[0]) or len(c) < 6:
            continue
        row = dict(zip(head, c))
        bad, words = row.get('rejected wording', ''), row.get("user's words", '')
        if words.strip().lower() in ('same', 'as above'):  # the table writes "same" for the row above's words
            words = prev
        prev = words
        u.add('user_flag', c[0], f'{rel(FLAGS)}#bộ-test-câu-người-dùng-đã-chê:{ln}', t=f'{bad} | {words}',
              x=f"{row.get('context', '')} {row.get('facts to convey', '')}", register=row.get('register', ''),
              bad=bad, note=words, extra={'context': clean(row.get('context', '')),
                                          'facts': clean(row.get('facts to convey', ''))})


# ---------- references/corpus/*.md and *.jsonl ----------

EXC_ID = re.compile(r'^(?:>\s*)?\*\*([0-9]*[A-Z]+\d{2})(?:\.\*\*|\*\*\.?|\s*[—–-]\s*(.+?)\*\*)\s*(.*)$')
CORPUS_REGISTER = {'but-ky': 'memoir', 'loi-binh': 'narration', 'sach-su': 'formal', 'mach-ke': 'memoir'}


def corpus_stem(path):
    return re.sub(r'^corpus-|-corpus$', '', path.stem)


def source_table(lines):
    """Map source code (first cell) or title words → URL from '| code | title | url |' tables."""
    codes, rows = {}, []
    for raw in lines:
        if raw.startswith('|') and URL.search(raw):
            c = cells(raw)
            url = URL.search(raw).group(0)
            codes[clean(c[0])] = url
            rows.append((clean(raw).lower(), url))
    return codes, rows


def parse_corpus_md(u, path):
    stem, lines = corpus_stem(path), nfc(path.read_text()).split('\n')
    codes, rows = source_table(lines)
    register = CORPUS_REGISTER.get(stem, 'narration')
    anchor, h3, mode, n = '', '', '', {}
    i = 0

    def h3_url():
        title = re.findall(r'\*([^*]+)\*', h3)
        for key in title:
            for row, url in rows:
                if key.lower() in row:
                    return url
        return ''

    while i < len(lines):
        raw, ln = lines[i], i + 1
        if raw.startswith('## '):
            anchor, h3 = slug(raw[3:]), ''
            low = raw.lower()
            mode = 'avoid' if 'sáo' in low else 'naming' if 'cách gọi' in low else ''
            i += 1
            continue
        if raw.startswith('### '):
            h3 = clean(raw[4:])
            i += 1
            continue
        src = f'{rel(path)}#{anchor}:{ln}'
        m = EXC_ID.match(raw.strip())
        if m and not mode:
            eid, label, rest = m.group(1), clean(m.group(2) or ''), m.group(3)
            block, j = [], i + 1
            while j < len(lines) and not lines[j].startswith('#') and not EXC_ID.match(lines[j].strip()):
                block.append(lines[j])
                j += 1
            quote, notes, url = [], [], ''
            note_in_line = re.search(r'\]\s*$', rest) and re.search(r'\s\[([^\[\]]+)\]\s*$', rest)
            if note_in_line:
                notes.append(note_in_line.group(1))
                rest = rest[:note_in_line.start()]
            if rest.strip():
                quote.append(rest)
            for b in block:
                s = b.strip()
                is_quote = s.startswith('>')
                s = s.lstrip('>').strip()
                if not s:
                    continue
                found = URL.search(s)
                if found and not url:
                    url = found.group(0)
                if re.match(r'(\*?URL|Nguồn)\b', s):
                    ref = re.search(r'\[(\w+)\]', s)
                    if ref and not url:
                        url = codes.get(ref.group(1), '')
                    continue
                if is_quote and not re.match(r'\*[^*]+:\*', s):
                    quote.append(s)
                else:
                    notes.append(re.sub(r'URL:.*$', '', s))
            text = unquote(' '.join(quote))
            if not url:
                prefix = re.match(r'[0-9]*[A-Z]+?(?=\d{2}$)', eid)
                url = codes.get(prefix.group(0) if prefix else '', '') or h3_url()
            note = clean(' '.join(notes))
            if text:
                u.add('excerpt', f'{stem}:{eid}', src, t=text, x=f'{label} {note} {h3}', register=register,
                      text=text, note=label or note,
                      extra={'source': h3, 'url': url})
            i = j
            continue
        if mode == 'naming' and raw.startswith('|') and not re.match(r'\|\s*-', raw):
            c = cells(raw)
            if len(c) >= 3 and not re.match(r'(concept|khái niệm|ý trong đầu)', c[0], re.I):
                n['naming'] = n.get('naming', 0) + 1
                u.add('naming', f'name:{stem}.{n["naming"]}', src, t=f'{c[1]} | {c[2]}', x=c[0],
                      register=register, text=c[1], note=c[2], extra={'concept': clean(c[0])})
        elif mode == 'avoid' and (raw.startswith('- ') or
                                  (raw.startswith('|') and not re.match(r'\|\s*-', raw))):
            c = cells(raw) if raw.startswith('|') else [raw[2:]]
            if not re.match(r'(cụm nguyên văn|phrase)', c[0], re.I):
                n['avoid'] = n.get('avoid', 0) + 1
                body = clean(' — '.join(x for x in c if x))
                phrase = clean(body.split(':', 1)[0] if raw.startswith('- ') else cells(raw)[0])
                u.add('avoid', f'avoid:{stem}.{n["avoid"]}', src, t=body, text=phrase,
                      note=body[len(phrase):].lstrip(' :—'))
        i += 1


KINDS = {'pattern', 'pair', 'keep', 'overcorrection', 'excerpt', 'naming', 'avoid', 'connective', 'user_flag'}


def parse_corpus_jsonl(u, path):
    for ln, raw in enumerate(nfc(path.read_text()).split('\n'), 1):
        if not raw.strip():
            continue
        try:
            r = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f'skip {rel(path)}:{ln}: {e}', file=sys.stderr)
            continue
        kind = r.get('kind') if r.get('kind') in KINDS else 'excerpt'
        text, tags = r.get('text', ''), ' '.join(r.get('tags') or [])
        bad, nat = r.get('bad', ''), r.get('natural', '')
        if kind == 'pair' and not bad:  # contract text "BAD: x → GOOD: y" or "x → y"
            left, _, right = text.partition('→')
            bad, nat = re.sub(r'^\s*BAD:\s*', '', left), re.sub(r'^\s*GOOD:\s*', '', right)
        pids = PAT_ID.findall(f"{tags} {r.get('note', '')}")
        u.add(kind, str(r.get('id') or f'{path.stem}:{ln}'), f'{rel(path)}:{ln}',
              t=f'{bad} | {nat}' if bad else text, x=f"{tags} {r.get('note', '')} {r.get('source', '')}",
              pid=pids[0] if pids else '', pids=pids, register=r.get('register', ''), bad=bad, natural=nat,
              text=text, note=r.get('note', ''),
              extra={'source': r.get('source', ''), 'url': r.get('url', '')})


# ---------- build ----------

def sources():
    return ([REF / 'pairs.md', REF / 'patterns.md', REF / 'cach-goi.md', REF / 'connectives.md', FLAGS]
            + sorted(CORPUS.glob('*.md')) + sorted(CORPUS.glob('*.jsonl')))


def collect():
    u = Units()
    parse_pairs(u)
    parse_patterns(u)
    parse_cach_goi(u)
    parse_connectives(u)
    parse_flags(u)
    for p in sorted(CORPUS.glob('*.md')):
        parse_corpus_md(u, p)
    for p in sorted(CORPUS.glob('*.jsonl')):
        parse_corpus_jsonl(u, p)
    return u.rows


SCHEMA = """
CREATE TABLE units(id INTEGER PRIMARY KEY, uid TEXT UNIQUE, kind TEXT, pid TEXT, pids TEXT, register TEXT,
                   bad TEXT, natural TEXT, text TEXT, note TEXT, extra TEXT, src TEXT, t TEXT);
CREATE INDEX units_kind ON units(kind);
CREATE VIRTUAL TABLE fts USING fts5(t, g, x, content='',
                                    tokenize="unicode61 remove_diacritics 0 tokenchars '_'");
"""


def build(db=DB):
    rows = collect()
    tmp = db.with_name(f'{db.stem}.tmp{os.getpid()}')  # per process: two readers may rebuild at once
    tmp.unlink(missing_ok=True)
    con = sqlite3.connect(tmp)
    con.executescript(SCHEMA)
    for i, r in enumerate(rows, 1):
        con.execute('INSERT INTO units VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    (i, r['uid'], r['kind'], r['pid'], r['pids'], r['register'], r['bad'], r['natural'],
                     None if r['text'] == clean(r['t']) else r['text'], r['note'], r['extra'], r['src'], r['t']))
        con.execute('INSERT INTO fts(rowid, t, g, x) VALUES (?,?,?,?)', (i, r['t'], grams(r['t']), r['x']))
    con.execute("INSERT INTO fts(fts) VALUES ('optimize')")
    con.commit()
    con.execute('VACUUM')
    con.close()
    tmp.replace(db)
    return rows


def stale(db=DB):
    if not db.exists():
        return True
    t = db.stat().st_mtime
    return any(p.stat().st_mtime > t for p in sources() + [Path(__file__)])


def vectors(download=False):
    """Refresh rag/viet_vec.db; one status line. Without the model (and no --vectors) it only says so."""
    sys.dont_write_bytecode = True
    import vec
    why = vec.missing_libs()
    if why:
        return f'vectors: skipped, {why}'
    if not vec.have_model():
        if not download:
            return 'vectors: model not downloaded, keyword only (python3 rag/build.py --vectors)'
        vec.download()
    n, new, sec = vec.refresh(log=print)
    return f'built {rel(vec.VDB)}: {n} units, {new} embedded with {vec.NAME}, {sec:.1f} s'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--stats', action='store_true', help='print unit counts per kind and the DB sizes')
    ap.add_argument('--vectors', action='store_true', help='download the embedding model if missing')
    args = ap.parse_args()
    rows = build()
    if args.stats:
        con = sqlite3.connect(DB)
        for kind, n in con.execute('SELECT kind, count(*) FROM units GROUP BY kind ORDER BY count(*) DESC'):
            print(f'{kind:15} {n:5}')
        print(f'{"total":15} {len(rows):5}')
        print(f'sources: {len(sources())} files ({len(list(CORPUS.glob("*.jsonl")))} jsonl)')
        print(f'{rel(DB)}: {DB.stat().st_size / 1024:.0f} KiB')
    else:
        print(f'built {rel(DB)}: {len(rows)} units')
    print(vectors(args.vectors))
    vdb = RAG / 'viet_vec.db'
    if args.stats and vdb.exists():
        print(f'{rel(vdb)}: {vdb.stat().st_size / 1024:.0f} KiB')


if __name__ == '__main__':
    main()
