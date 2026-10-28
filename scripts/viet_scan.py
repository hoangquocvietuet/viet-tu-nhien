#!/usr/bin/env python3
"""Triage scanner for English-shaped Vietnamese ("văn dịch", "câu Tây"). Part of skill viet-tu-nhien.

  python3 viet_scan.py FILE|-            [--register narration|chat|doc] [--json]
  python3 viet_scan.py --selftest

A hit is a prompt to reread one sentence with a native ear, never proof of a calque and never a
rewrite: the scanner does not change text and always exits 0. Pattern ids match
../references/patterns.md. Patterns whose single hit means nothing (một, của, được, các/những,
essay connectives) only report when a paragraph holds at least DENSITY[id] of them.
Other scripts and RAG tools import PATTERNS / scan_text (rag/viet_rag.py does).
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

INFO, WARN = 'info', 'warn'
CAP = r'(?-i:[A-ZĐÂĂÊÔƠƯÁÀẢÃẠÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌÚÙỦŨỤÝỲỶỸỴ])'  # capital letter: start of a name

# (id, regex, severity, note). An id may own several regexes. Ids and names: references/patterns.md.
PATTERNS = [
    # A. Sentence frame and subject
    ('A01', r'\b(cái|thứ) gì (giữ|làm|khiến|quyết định|giúp)', WARN,
     'abstract wh-subject ("what keeps…"): put the concrete thing first, ask "nhờ đâu / vì sao"'),
    ('A01', r'(?:^|[.!?]\s+)những gì\b', INFO, '"những gì…" as subject ("what the sources record"): start from the thing itself'),
    ('A03', r'(?:^|[.!?,]\s*)(thứ|cái|điều) (có thật|quan trọng|đáng nói|đáng chú ý|\w+ (giữ|cần|muốn|làm|thấy)) là\b', WARN,
     'cleft "the thing that … is": say the action with its doer'),
    ('A04', r'\blà (thứ|điều|cái|người|nơi) mà\b', WARN, '"là thứ mà" relative clause: topic first, then the comment'),
    ('A05', r'(?:^|[.!?]\s+)(không )?có (?!điều\b)[^.!?,\n]{1,40} (ở|tại) (đây|đó|\w+)', INFO,
     '"there is X in Y" order: put the place first ("Ở đây có…")'),
    ('A05', r'\btồn tại (trong|ở|tại)\b', INFO, '"tồn tại" copied from "exist / there is"'),
    ('A06', r'\b(người|nơi|điều|thứ|chỗ|lúc) mà (tôi|ông|bà|họ|ta|chúng ta|người ta|anh|chị|em|mình|bạn)\b', INFO,
     '"who/that" copied as "mà": the clause usually needs no linker'),
    ('A07', r', tức (là )?[^,.\n]{4,80}(,|$)', INFO,
     'gloss wedged mid-sentence or repeating a quote ("X, i.e. Y, V…"): move it, or drop it if viewers know the word'),
    ('A07n', r'\btức là\b', INFO, 'several "tức là" in one paragraph: keep only the glosses a listener needs'),
    ('A09', r'\b(sau khi|trước khi|tới khi|đến khi)\b', INFO,
     'English time clause ("after/before/since"): "lúc đã…", "từ lúc…", "tới lúc…", or tell in order'),
    ('A09', r'(?:^|[.!?]\s+)(rồi )?(khi|để) [^.!?\n]{3,60},', INFO,
     'fronted "When…, / To…," clause: "Muốn… thì…", "Tới…", or put the scene first'),
    ('A10', r'\bvà đó là\b|, nơi (sau này|về sau)', INFO, 'English tail ("and that was…", ", where later…"): "thế là…", or a new clause'),
    ('A13', r'\bkể từ (khi|lúc)\b', INFO, '"since": "từ lúc…", "tính từ lúc…"'),
    ('A11', r'(?:^|[.!?]\s+)(ông ấy|bà ấy|anh ấy|cô ấy|họ|nó)\b[^.!?\n]*[.!?]\s+\1\b', WARN,
     'same pronoun opens consecutive sentences (English needs a subject, Vietnamese drops it)'),
    ('A12', r'[^.!?\n]*(,(?!\s*\d)[^,.!?\n]*){4,}[.!?]?', INFO, 'four or more commas in one sentence: split where the listener can hold the topic'),
    # B. Function words copied one by one
    ('B01', r'\blà một (?!(trong|lần|nửa|phần|ít|chút|số|vài|mình)\b)\w+', INFO,
     '"là một" = "is a": drop "một" unless it counts or introduces'),
    ('B01n', r'\bmột\b(?!\s+(lần|lúc|chút|ít|số|vài|trong|mình|nửa|khác|phần|thời|hai|bên|câu|người|hôm|ngày|năm|tháng)\b)', INFO,
     'many "một" in one paragraph: English articles leaking'),
    ('B02', r'(?<!còn )(?<!đúng )(?<!thêm )(?<!yên )\bmột (tòa thành|kinh đô|triều đình|pháo đài|đô thị|thành quân sự|ông vua|tờ chiếu|thung lũng|nơi|chỗ|vùng|cuộc|lý do)\b(?![^.,\n]{0,20}\bkhác\b)', WARN,
     '"một" as English "a" before a place/institution/event noun: drop it, or use "… ấy", "nào"'),
    ('B03', r'\bmột cách\b', WARN, '"một cách + adj" = English "-ly": use the adjective/verb directly'),
    ('B04', r'(?:^|[.!?]\s+)một (phải|nên|cần|có thể) ', WARN, 'generic "one must": "ta / người ta / người đọc"'),
    ('B05', r'\bnó\b', WARN, '"nó" for a thing/place/idea ("it"): repeat the noun, use "ấy", or drop the subject'),
    ('B06', r'\bnó (được|là) (công nhận|cho rằng|cho là|biết|quan trọng|cần thiết)', WARN, 'dummy "it is … that": "người ta…", or the clause itself'),
    ('B07', r'\bchúng (bảo vệ|giúp|cho phép|được|là|có|vẫn|đã|đang)\b', INFO, '"chúng" for things ("they"): repeat the noun or drop it'),
    ('B08', r'\b(các|những) (người dân|dân chúng|nhân dân)\b|\blà những\b', WARN, 'plural "các/những" copied from English -s'),
    ('B08n', r'\b(các|những)\b', INFO, 'many "các/những" in one paragraph: English plural leaking'),
    ('B09', r'\bcủa\b[^.,;:!?\n]{1,30}\bcủa\b', WARN, '"of … of" chain: compound the nouns or turn one into a verb'),
    ('B09n', r'\bcủa\b', INFO, 'many "của" in one paragraph: possession only where it is the point'),
    ('B10', r'\bcủa (nhà|họ|nước|triều) ' + CAP, INFO, '"của" before a dynasty/clan/country: "kinh đô nhà Hồ", "vua nước Nam Việt"'),
    ('B10', r'\b(kinh đô|thủ đô|đất gốc|vua|vua đầu tiên|xã|vùng|huyện|tỉnh|phủ) (' + CAP + r'[^,.\n]{0,20} )?của ' + CAP, INFO,
     '"X của <name>": "xã Đông Anh ở Hà Nội", "kinh đô nhà Nguyễn"'),
    ('B11', r'\bvới (vòng|ba|hai|bốn|năm|mười|một|những|các) ', INFO, '"với" = "with" (equipment, parts): "có", or a new clause'),
    ('B11', r'\b(khởi công|bắt đầu|mở đầu|kết thúc|xây)\b[^.,\n]{0,25}\bvới\b', WARN, '"started with / ended with": tell what it had'),
    ('B12', r'\b(được|bị) [^.,;!?\n]{1,40}\bbởi\b', WARN, 'passive with "bởi" agent ("was V-ed by"): put the doer first'),
    ('B13', r'\bđã\b[^.!?\n]{0,40}\bđang\b|\bđang được\b', INFO, 'English tense stack: Vietnamese marks time once, by context or "còn/đã"'),
    ('B14', r'\b(khó|dễ|quan trọng|cần thiết|cố gắng|cố) để \w+', INFO, '"hard/easy to V" with "để": "khó V", "dễ V", "cố V"'),
    # C. Passive and the hidden doer
    ('C01', r'\bđược (\w+ ){0,2}?(khởi công|xây|xây dựng|chọn|ghi lại|chép lại|thực hiện|tiến hành|triển khai|kiểm lại|kiểm tra|phát hiện|tìm thấy|đưa ra|công bố|hoàn thành|cập nhật|xử lý|sửa)\b', WARN,
     'passive "được + V" hides who did it: name the doer, or drop "được" ("khởi công năm…")'),
    ('C01n', r'\bđược\b', INFO, 'many "được" in one paragraph: check each for a hidden doer'),
    ('C02', r'(?:^|[.!?]\s+)(được|bị) [^.!?\n]{2,60}\brằng\b|\bđược (khuyến cáo|khuyên|khuyến nghị) nên\b', WARN,
     'impersonal passive ("it is recognized that"): "người ta…", "nên…"'),
    ('C03', r'\b(sợ|khó|dễ) bị \w+', INFO, '"afraid of being / hard to be V-ed": name the attacker ("sợ giặc đánh tới")'),
    ('C04', r'\b(sẽ|đã|đang) được (kiểm|xử lý|cập nhật|thêm|sửa|làm|gửi|chạy|kiểm tra|xem|duyệt|ghi|đẩy|tạo)\b', WARN,
     'status in the passive ("will be checked"): say who does it ("mình sẽ kiểm lại")'),
    ('C05', r'\bđã (được )?\w+ (thì )?sẽ được \w+|\bđã được \w+ (thì )?(sẽ )?được\b', WARN,
     'double passive ("an approved stage will be reopened"): "đã duyệt thì mở lại", or name who acts'),
    # D. Nominalisation and light verbs
    ('D01', r'\b(cho|của|trong|về|với|vào) việc \w+|(?:^|[.!?]\s+)(việc|sự) \w+|\bsự \w+ của\b', WARN,
     '"việc/sự + V" (the V-ing of): use the verb with its doer'),
    ('D02', r'\b(tiến hành|thực hiện|có sự|đưa ra (một )?(quyết định|lời|câu trả lời|nhận xét|đánh giá))\b', WARN,
     'light verb + noun ("conduct, carry out, make a decision"): the main verb alone'),
    ('D04', r'\blý do (tại sao|vì sao)\b|\bcách (thức )?mà\b', INFO, '"the reason why / the way that": ask or state the cause directly'),
    ('D06', r'\b(những )?lợi ích của (việc|sự)\b', WARN, '"the benefits of V-ing": use the verb ("đem cái học về cho họ")'),
    ('D05', r'(?:^|[.!?]\s+)(đó|đây) là (chọn|việc|cách|sự)\b', INFO, '"That is choosing…" (gerund predicate): tell what was done'),
    # E. English frames, idioms and logic
    ('E01', r'đóng (một )?vai trò|chơi (một )?vai trò|mở ra (một )?(chương|trang) mới|số phận khác|kẻ thù đến từ|đặt [^.\n]{0,40}lên cùng một|'
            r'rơi vào tình yêu|xây dựng một (kỳ|kì) nghỉ|chủ đề tốt để|(là|nắm giữ) chìa khóa|trải qua cả một|duy nhất từng|'
            r'không bao giờ (thành|trở thành)|ra khỏi mặt trời|ở cuối ngày|trên cùng một trang|đi kèm với|ở một mức độ nào đó|'
            r'trong bối cảnh|điều quan trọng (là|cần)|tạo ra sự khác biệt|có chung một sợi chỉ|soi [^.\n]{0,25}(vào|về|ngược về) [^.\n]{0,12}(năm|đời|chặng|quãng|thời)', WARN,
     'English idiom or frame translated word by word: say what happened, in the words a Vietnamese speaker uses'),
    ('E02', r'\b(điều|việc|sự|chuyện|phản biện|góp ý|review|lỗi|nó|điều này|đó|này|ấy) (này |đó |ấy )?(khiến|làm cho|dẫn tới|dẫn đến)\b', WARN,
     'English causative ("X made me / led to"): tell the event, then what followed'),
    ('E02', r'\bdẫn (tới|đến) (một|việc|sự)\b|\b(khiến|làm cho) (cho )?(mình|tôi|chúng tôi) (phải )?(sửa|đổi|nghĩ|thấy|quyết định)\b', WARN,
     'English causative ("led to a…", "made me fix"): "sau đó…", "nên mình sửa…"'),
    ('E03', r'\b(này|đó|ấy|nó) là (rất |khá |cực kỳ |vô cùng )?(quan trọng|cần thiết|khả thi|hữu ích|đúng|sai|tốt|dễ|khó|rõ ràng|hiệu quả|phổ biến)\b', INFO,
     '"is + adjective": Vietnamese adjectives are predicates; drop "là"'),
    ('E04', r'\bhơn [^.,!?\n]{1,30} rất nhiều\b|\bkhó bị \w+ hơn\b|\bxa gấp [^.,\n]{0,15}lần ' + CAP + r'|\b(nhiều|ít|cao|thấp|lớn|nhỏ|lâu) hơn so với\b', WARN,
     'English comparative ("much longer than", "harder to be V-ed"): "… làm sao bì được", "dễ giữ hơn", compare like with like'),
    ('E05', r'\bkhông (chỉ|những) [^.!?\n]{1,80}\bmà còn\b', INFO, '"not only … but also" used for rhythm: plain statement or a real contrast'),
    ('E08', r'\btên của (bạn|anh|chị|em|ông|bà) là gì', WARN, 'question translated word by word: "Bạn tên gì?"'),
    ('E09', r'\bbiến [^.,!?\n]{1,30} thành (nơi|chỗ|một)\b', INFO, '"turn X into a place": "lấy X làm nơi…"'),
    ('E11', r'\btrong (mối )?quan hệ (với|đối với)\b', WARN, '"in relation to": say what the relation is, or restructure'),
    ('E12', r'\bvới tư cách( là)?\b', INFO, '"as a …": "làm …", "vào làm …" (native in formal register)'),
    ('E13', r'\bsử dụng\b', INFO, '"use" in speech: "dùng"'),
    # F. Connectives, hedges, signposting
    ('F01', r'(?:^|[.!?:]\s+)(tuy nhiên|do đó|bên cạnh đó|ngoài ra|hơn nữa|mặt khác|vì vậy|nhìn chung|tóm lại|nói cách khác|trên thực tế|đáng chú ý là)\b', WARN,
     'essay connective in speech: "nhưng", "nên", "thế là", "còn", or nothing'),
    ('F01n', r'\b(nhằm|đối với|bên cạnh đó|ngoài ra|do đó|tuy nhiên)\b', INFO, 'many essay connectives in one paragraph'),
    ('F02', r'\b(có lẽ|có thể|nhiều khả năng|dường như|có vẻ|phần nào)\b[^.!?,\n]{0,15}\b(có thể|phần nào|có lẽ|dường như|có vẻ|nhiều khả năng)\b', WARN,
     'stacked hedges: state the certainty the source allows, once'),
    ('F03', r'\bnhiều khả năng (là )?(do|vì)\b|\bcó khả năng cao\b', INFO, 'translated hedge ("most likely due to"): "tôi nghĩ phần lớn là vì", "có lẽ"'),
    ('F05', r'\b(hãy cùng|cùng (nhau )?tìm hiểu|cùng khám phá|như (các )?bạn (có thể )?thấy|trong bài viết này|dưới đây là|sau đây là|chắc chắn rồi|'
            r'hy vọng (điều này|thông tin|bài viết)|nếu bạn cần thêm|đừng ngần ngại|trong thời đại|bạn có biết|mời (các )?bạn)\b', WARN,
     'chatbot / video-essay signposting: start with the content'),
    ('F08', r'\bđồng thời\b', INFO, '"and at the same time" as a connective: "và", or two sentences'),
    # G. Chat replies
    ('G01', r'^[ \t]*(?:[-*+]|\d+[.)])?[ \t]*(?:\*\*)?(hỏi|trả lời|mở|kết|sợi lặp|bài học|mục tiêu|kết quả|lưu ý|tóm tắt|vấn đề|giải pháp|nguyên nhân|trạng thái|ưu điểm|nhược điểm|bước tiếp theo)(?:\*\*)?[ \t]*:', WARN,
     'label-colon line ("Hỏi:", "Kết quả:"): write the sentence the label stands for'),
    ('G01', r'^[ \t]*(?:[-*+]|\d+[.)])[ \t]+\*\*[^*\n]{1,60}\*\*|\*\*[^*\n]{1,40}:\*\*|\*\*[^*\n]{1,40}\*\*:', WARN,
     'bold-label list: tell it in sentences'),
    ('G03', r'\bđã qua (hai|ba|bốn|\d+|nhiều) (lượt|vòng)\b|(?:^|[.!?]\s+)kết quả (đo được|thu được|kiểm tra)?\s*(là|:)|\bkết quả đo được\b|'
            r'\b(phản biện|review|góp ý|kiểm tra|đánh giá) (khiến|giúp|làm cho) (mình|tôi)\b', WARN,
     'English-shaped status line ("passed two rounds of review", "Results measured:"): say who did what'),
]

# Ids whose single hit is no evidence: report only at >= N hits in one paragraph.
DENSITY = {'A07n': 2, 'B01n': 4, 'B08n': 5, 'B09n': 4, 'C01n': 4, 'F01n': 3}

# Registers. narration: spoken script heard once (voice-over, video, podcast; default). chat: a reply to a person.
# doc: README, notes, reports, formal prose, where essay connectives and some nominalisation are normal.
REGISTER_OFF = {
    'narration': {'G01', 'G03', 'C04', 'F08'},
    'chat': set(),
    'doc': {'G01', 'G03', 'F01n', 'B09n', 'C01n', 'E13'},
}
REGISTER_INFO = {  # downgraded to info in that register
    'narration': set(),
    'chat': {'A09', 'B05'},
    'doc': {'F01', 'C01', 'D01', 'D02', 'B05'},
}

COMPILED = [(pid, re.compile(rx, re.I | re.M), sev, note) for pid, rx, sev, note in PATTERNS]
CODE = re.compile(r'```.*?```|`[^`\n]*`|https?://\S+', re.S)


def nfc(text):
    return unicodedata.normalize('NFC', text)


def blank(match):
    return re.sub(r'[^\n]', ' ', match.group(0))


def sentence_at(text, start, end):
    a = max(text.rfind(c, 0, start) for c in '.!?\n')
    z = [i for i in (text.find(c, end) for c in '.!?\n') if i >= 0]
    return text[a + 1:(min(z) + 1) if z else len(text)].strip()


def scan_text(text, register='narration', skip=(), unit='p1', line0=1):
    """Findings for one paragraph/unit of text. Density ids report once per unit, at the first hit."""
    text = nfc(text)
    if register in ('chat', 'doc'):
        text = CODE.sub(blank, text)
    off, down = REGISTER_OFF[register], REGISTER_INFO[register]
    found, seen = [], set()
    for pid, rx, sev, note in COMPILED:
        if pid in off or pid in skip:
            continue
        hits = list(rx.finditer(text))
        if not hits:
            continue
        if pid in DENSITY:
            if len(hits) < DENSITY[pid]:
                continue
            hits, note = hits[:1], f'{note} ({len(hits)} in this paragraph)'
        for m in hits:
            s, e = m.span()
            while s < e and text[s] in ' .!?:,\n\t':
                s += 1
            if (pid, s) in seen:
                continue
            seen.add((pid, s))
            found.append({'id': pid, 'severity': INFO if pid in down else sev, 'unit': unit,
                          'line': line0 + text.count('\n', 0, s), 'start': s, 'end': e,
                          'match': text[s:e].strip(), 'sentence': sentence_at(text, s, e), 'note': note})
    return sorted(found, key=lambda f: (f['line'], f['start']))


def units_from_text(text):
    """Blank-line separated paragraphs as (unit id, first line, text)."""
    out, line, buf, start = [], 1, [], 1
    for raw in nfc(text).split('\n') + ['']:
        if raw.strip():
            if not buf:
                start = line
            buf.append(raw)
        elif buf:
            out.append((f'p{len(out) + 1}', start, '\n'.join(buf)))
            buf = []
        line += 1
    return out


def scan_units(units, register):
    findings = []
    for uid, line0, text in units:
        findings += scan_text(text, register, unit=uid, line0=line0 or 1)
    return findings


def print_plain(findings):
    for f in findings:
        where = f"{f['line']}:{f['unit']}"
        print(f"{where} [{f['severity']}] {f['id']} «{f['match'][:60]}» {f['note']}")
        print(f"    {f['sentence'][:200]}")
    counts = {}
    for f in findings:
        counts[f['id']] = counts.get(f['id'], 0) + 1
    warn = sum(f['severity'] == WARN for f in findings)
    print(f"{len(findings)} cue(s): {warn} warn, {len(findings) - warn} info; by id: "
          + (', '.join(f'{k} {v}' for k, v in sorted(counts.items())) or 'none'))
    print('Triage only: reread each flagged sentence aloud; keep it if a Vietnamese speaker would say it.')


# Self-test: real pairs from references/pairs.md (bad, natural) per pattern id, plus sentences reviewers
# kept as natural. "(minh họa)" in pairs.md marks the few illustrative ones; they are kept out of this table.
SELFTEST = [
    ('A01', 'narration', 'Vậy không phải bức tường thì rốt cuộc cái gì giữ được một kinh đô?', 'Vậy không phải nhờ bức tường thì rốt cuộc kinh đô đứng được lâu là nhờ đâu?'),
    ('A01', 'narration', 'Cái gì giữ một kinh đô', 'Không phải nhờ bức tường'),
    ('A01', 'narration', 'Những gì sử sách còn ghi về Hai Bà nằm trong dăm cuốn sách', 'Chuyện Hai Bà nay chỉ còn chép trong dăm cuốn sách'),
    ('A03', 'narration', 'Thứ có thật là kho tên Cầu Vực, nơi tìm thấy khoảng mười nghìn mũi tên đồng.', 'Ngoài đời thật thì có kho tên Cầu Vực, nơi đào được khoảng mười nghìn mũi tên đồng.'),
    ('A03', 'narration', 'rút khỏi thành, tôi thấy lời ấy khá khớp, cái họ giữ là dân với lương còn cái thành thì họ bỏ lại.', 'rút khỏi thành mới thấy lời ấy đúng thật, vì họ giữ lấy dân với lương còn thành thì bỏ lại.'),
    ('A04', 'narration', 'Loại táo này là thứ mà tôi rất thích ăn.', 'Loại táo này tôi rất thích ăn.'),
    ('A05', 'narration', 'Không có mặt trời ở đây.', 'Ở đây không có nắng.'),
    ('A05', 'narration', 'Có nhiều xe máy ở Việt Nam.', 'Ở Việt Nam có nhiều xe máy.'),
    ('A06', 'narration', 'Người mà tôi gặp hôm qua là nhà văn.', 'Người tôi gặp hôm qua là nhà văn.'),
    ('A07', 'narration', 'Lúc ấy thái thú, tức viên quan nhà Hán cai cả một quận, cùng các quan Hán khác chỉ còn', 'Trong khi đó các quan Hán ở đây, kể cả những thái thú cai cả một quận, chỉ còn'),
    ('A07', 'narration', 'thế cô, đều thua chết, tức là lẻ loi yếu thế và cả hai đều thua mà chết', 'thế cô nên cả hai đều thua mà chết'),
    ('A09', 'narration', 'Một người nói sau khi thắng,', 'Một người nói lúc đã thắng,'),
    ('A13', 'narration', 'kể từ khi cảnh người Việt đánh nhau trong nhà vừa dứt.', 'tính từ lúc người Việt thôi đánh nhau trong nhà.'),
    ('A13', 'doc', 'Nếu file đã bị thay đổi kể từ lúc tải, endpoint trả về lỗi 409.', 'Nếu file đã đổi từ lúc được tải lên màn hình, endpoint trả 409 và không ghi gì.'),
    ('A09', 'narration', 'mà rút đi trước khi giặc tới,', 'mà rút đi từ lúc giặc chưa tới,'),
    ('A09', 'narration', 'Rồi khi quân tới Tam Điệp, ông gọi', 'Tới Tam Điệp, ông gọi'),
    ('A09', 'narration', 'và ở đó sáu năm tới khi mất năm 944.', 'và ở đó sáu năm tới lúc mất năm 944.'),
    ('A09', 'narration', 'Để biết một kinh đô gần hay xa phương bắc, ta đo', 'Muốn biết kinh đô nào gần hay xa phương bắc thì ta đo'),
    ('A10', 'narration', 'và đó là lần đầu tiên Thăng Long', 'thế là lần đầu tiên Thăng Long'),
    ('A10', 'narration', 'Đó là cửa sông Hương thông ra biển, nơi sau này hạm đội Pháp kéo vào.', 'Đó là cửa sông Hương thông ra biển, về sau hạm đội Pháp kéo vào chính từ đây.'),
    ('B01', 'narration', 'Hoa Lư là một thung lũng phẳng giữa núi đá vôi dựng đứng,', 'Hoa Lư là thung lũng phẳng lọt giữa núi đá vôi dựng đứng,'),
    ('B01', 'narration', 'Anh ấy là một bác sĩ.', 'Anh ấy là bác sĩ.'),
    ('B01', 'narration', 'mà thành phố vẫn là một đô thị lớn.', 'mà phố xá vẫn đông nghịt người.'),
    ('B01', 'narration', 'Hoa Lư không mất vì thua trận, mà là triều đình tự bỏ đi, và về sau nơi này vẫn là một thành quân sự quan trọng.', 'Hoa Lư không mất vì thua trận mà vì triều đình tự bỏ đi, và về sau nơi này vẫn là chỗ đóng quân quan trọng.'),
    ('B02', 'narration', 'nên đây là chỗ yên ổn cho một triều đình vừa qua nội chiến.', 'nên triều đình vừa qua nội chiến ngồi ở đây thấy yên ổn.'),
    ('B02', 'narration', 'xây trên nền một tòa thành cũ.', 'xây chồng lên nền thành cũ.'),
    ('B02', 'narration', 'nên quân Nguyên vào chỉ thấy một tòa thành không có lương.', 'nên quân Nguyên vào tới nơi chỉ thấy thành không, kho chẳng có lương.'),
    ('B02', 'narration', 'triều đình lại về núp sau một pháo đài.', 'triều đình lại về núp sau pháo đài.'),
    ('B02', 'narration', 'một tờ chiếu ngắn gửi cho cả triều đình đọc.', 'rồi cho đọc trước cả triều đình, chiếu ấy ngắn thôi.'),
    ('B02', 'narration', 'Đến cuối chiếu, một ông vua vừa lên ngôi lại hỏi ý cả triều bằng một câu rất ngắn:', 'Đến cuối chiếu, ông vua mới lên ngôi ấy lại quay sang hỏi cả triều đúng một câu:'),
    ('B02', 'narration', 'Lý Công Uẩn thì nói rõ một lý do vì dân khi chọn đất, một nơi rộng và cao ráo dù gần phương bắc hơn.', 'Lý Công Uẩn thì khi chọn đất đã nói rõ là vì dân, chọn chỗ rộng mà cao ráo dù gần phương bắc hơn.'),
    ('B03', 'doc', 'Caffeine được hấp thụ một cách nhanh chóng.', 'Caffeine ngấm vào máu nhanh.'),
    ('B05', 'narration', 'Người cho xây nó là', 'Người cho xây thành là'),
    ('B05', 'narration', 'dù tới giờ nó vẫn còn đứng đó.', 'dù tới giờ tường vẫn còn đứng đó.'),
    ('B05', 'narration', 'Theo tôi, đó là vùng đông dân và nhiều lúa ở quanh nó.', 'Theo tôi là nhờ vùng đông dân và nhiều lúa ở xung quanh.'),
    ('B05', 'narration', 'còn cái triều đình núp sau nó thì', 'còn triều đình núp sau bức tường ấy thì'),
    ('B05', 'narration', 'Vậy mà cộng lại, nó vẫn làm kinh đô hơn bảy trăm năm.', 'Vậy mà cộng lại thì vẫn làm kinh đô được hơn bảy trăm năm.'),
    ('B05', 'narration', 'Người quyết định bỏ nó mà đi là vua Lý Công Uẩn, ông vua đầu tiên của nhà Lý.', 'Người quyết định bỏ vòng núi ấy mà đi là Lý Công Uẩn, vua đầu tiên nhà Lý.'),
    ('B06', 'doc', 'Nó được công nhận rằng tỉ lệ thất nghiệp đã tăng.', 'Người ta thừa nhận tỉ lệ thất nghiệp đã tăng.'),
    ('B08', 'narration', 'Năm kinh đô này nhìn chung chia làm hai kiểu, mà kiểu thứ nhất là những pháo đài dựa vào lũy đất, núi đá hay tường đá để giữ mình.', 'Năm kinh đô này đại khái chia làm hai kiểu, kiểu thứ nhất là pháo đài dựa vào lũy đất, núi đá hay tường đá mà giữ mình.'),
    ('B10', 'narration', 'kinh đô của nhà Hồ lúc ấy.', 'lúc ấy là kinh đô nhà Hồ.'),
    ('B10', 'narration', 'chọn Huế làm kinh đô của nhà Nguyễn.', 'chọn Huế làm kinh đô nhà Nguyễn.'),
    ('B10', 'narration', 'lại là đất gốc của họ Nguyễn', 'lại là đất gốc họ Nguyễn'),
    ('B10', 'narration', 'Âu Lạc rơi vào tay Triệu Đà của nước Nam Việt.', 'Âu Lạc rơi vào tay Triệu Đà, vua nước Nam Việt.'),
    ('B10', 'narration', 'nay thuộc xã Đông Anh của Hà Nội,', 'nay là xã Đông Anh ở Hà Nội,'),
    ('B10', 'narration', 'tức vùng Từ Sơn của Bắc Ninh bây giờ,', 'tức vùng Từ Sơn ở Bắc Ninh bây giờ,'),
    ('B11', 'narration', 'Kinh thành Huế khởi công năm 1805 với vòng tường dài khoảng mười cây số, dọc tường có hai mươi bốn pháo đài.', 'Năm 1805 Kinh thành Huế khởi công, tường dài khoảng mười cây số và dọc tường có hai mươi bốn pháo đài.'),
    ('B11', 'narration', 'là Cổ Loa với ba vòng lũy đất,', 'là Cổ Loa có ba vòng lũy đất,'),
    ('B12', 'doc', 'Email đã được nhận bởi một số nhân viên.', 'Một số nhân viên đã nhận được email.'),
    ('B12', 'doc', 'Hệ thống được triển khai bởi đội kỹ thuật.', 'Đội kỹ thuật triển khai hệ thống.'),
    ('B13', 'narration', 'Chỉ tháng trước, những cây đã xanh, mà nay chúng đang vàng.', 'Mới tháng trước, cây cối còn xanh, mà nay đã vàng rực.'),
    ('B14', 'doc', 'Không khó để chứng minh rằng', 'Có thể dễ dàng chứng minh rằng'),
    ('C01', 'narration', 'được khởi công từ năm 1397,', 'khởi công từ năm 1397,'),
    ('C01', 'narration', 'còn Thăng Long thì được chọn để người các nơi kéo về', 'còn Thăng Long thì Lý Công Uẩn chọn để người các nơi kéo về'),
    ('C01', 'narration', 'Câu ông nói được Toàn thư ghi lại thế này:', 'Toàn thư chép lại câu ông nói thế này:'),
    ('C01', 'chat', 'Kết: Bác mất ngày 2/9/1969 nhưng được công bố là 3/9. Năm 1989 mới đính chính.', 'Bác mất ngày 2/9/1969, nhưng hồi đó công bố là ngày 3, tới năm 1989 mới nói lại cho đúng.'),
    ('C02', 'doc', 'Được công nhận rằng quá trình phân bào', 'Người ta công nhận quá trình phân bào'),
    ('C02', 'doc', 'Được khuyến cáo nên đến bác sĩ.', 'Bạn nên đến bác sĩ khám.'),
    ('C03', 'narration', 'Tôi đoán ông còn sợ bị đánh từ cả hai đầu đất nước,', 'Tôi đoán ông còn sợ giặc đánh tới từ cả hai đầu đất nước,'),
    ('C04', 'chat', 'Ngày tháng và chi tiết dưới đây sẽ được kiểm lại ở bước research.', 'Ngày tháng và chi tiết mình sẽ kiểm lại ở bước research.'),
    ('C05', 'doc', 'Khi lưu một thay đổi thật, stage research đã duyệt sẽ được mở lại.', 'và mở lại stage research nếu stage ấy đã approve.'),
    ('C05', 'doc', 'stage research đã được duyệt sẽ được mở lại', 'stage research đang ở trạng thái duyệt thì mở lại'),
    ('D06', 'narration', 'và đem lại cho họ những lợi ích của việc học.', 'rồi đem sự học ấy về cho họ.'),
    ('D01', 'narration', 'tiện cho việc làm ăn.', 'tiện đường làm ăn.'),
    ('D01', 'doc', 'Việc quản lý trở nên dễ dàng hơn.', 'Báo cáo tuần giờ có trong 15 phút thay vì cả buổi chiều.'),
    ('D02', 'narration', 'Nhà vua đã đưa ra một quyết định để tiến hành một cuộc tấn công.', 'Nhà vua quyết định đem quân đánh.'),
    ('D02', 'doc', 'Việc tiến hành thực hiện một cuộc khảo sát đã được hoàn tất.', 'Nhóm đã khảo sát xong.'),
    ('D05', 'chat', 'Trả lời: để khoảng 200.000 quân Tưởng rút về. Đó là chọn mối nguy nhỏ hơn cho lúc ấy.', 'Cho Pháp vào thì Tưởng phải rút, tức là đuổi được kẻ đáng ngại hơn.'),
    ('E01', 'narration', 'Đặt năm kinh đô lên cùng một tấm bản đồ từ Cổ Loa ngoài Bắc tới Huế ở miền Trung, ta thấy hai kiểu kinh đô có số phận khác hẳn nhau.', 'Chấm cả năm kinh đô lên bản đồ, từ Cổ Loa ngoài Bắc tới Huế ở miền Trung, thì thấy hai kiểu kinh đô đi hai ngả khác hẳn nhau.'),
    ('E01', 'narration', 'và lần này kẻ thù đến từ biển.', 'và lần này giặc kéo vào từ phía biển.'),
    ('E01', 'doc', 'Cà phê đóng vai trò vô cùng quan trọng trong thói quen hằng ngày.', 'Một ly cà phê buổi sáng giúp tỉnh người nhanh.'),
    ('E01', 'doc', 'Các tuyến nước nội địa có thể là một chủ đề tốt để xây dựng một kì nghỉ.', 'Du lịch bằng đường thủy nội địa là một ý tưởng nghỉ dưỡng không tồi.'),
    ('E01', 'narration', 'Ông vừa trải qua cả một cuộc nội chiến, nên tôi đoán', 'Nội chiến vừa mới dứt, nên tôi đoán'),
    ('E01', 'narration', 'Quân Thanh cũng chẳng phải đạo quân ngoại bang duy nhất từng vào thành,', 'Cũng đâu phải mỗi quân Thanh từng vào được thành này,'),
    ('E01', 'narration', 'và Nghệ An không bao giờ thành kinh đô.', 'và Nghệ An rốt cuộc chẳng thành kinh đô.'),
    ('E01', 'narration', 'Cúi xin bệ hạ bước ra khỏi mặt trời của kẻ hạ thần.', 'Tránh ra cho ta sưởi nắng.'),
    ('E01', 'chat', 'Cả chuỗi có chung một sợi chỉ là câu Bác dặn cụ Huỳnh Thúc Kháng năm 1946.', 'Cả chuỗi xoay quanh câu Bác nói năm 1946.'),
    ('E02', 'narration', 'Một tờ lo chuyện ruộng, một tờ lo chuyện trông coi đất nước, và chính tờ thứ hai dẫn tới một kinh đô mới.', 'Tờ thì lo ruộng, tờ thì lo trông coi đất nước, mà chính tờ thứ hai mới sinh chuyện dựng kinh đô mới.'),
    ('E02', 'chat', 'Phản biện khiến mình sửa những chỗ này so với bản đầu:', 'Grok và GPT đọc chéo xong, mình sửa mấy chỗ này so với bản đầu:'),
    ('E03', 'doc', 'Điều này là quan trọng đối với cuộc chiến.', 'Điều này quan trọng với cuộc chiến.'),
    ('E04', 'narration', 'hơn bảy trăm năm, lâu hơn Tây Đô rất nhiều.', 'hơn bảy trăm năm, Tây Đô làm sao bì được.'),
    ('E04', 'narration', 'Tây Đô khó bị đánh hơn,', 'Tây Đô dễ giữ hơn,'),
    ('E04', 'narration', 'xa gấp hơn bốn lần Thăng Long, nên giặc phương bắc muốn đánh tới cũng phải đi xa hơn nhiều.', 'gấp hơn bốn lần đường từ ải về Thăng Long, nên giặc phương bắc muốn đánh tới thì phải đi xa hơn nhiều.'),
    ('E05', 'doc', 'Không chỉ giúp tỉnh táo, cà phê mà còn mang lại nhiều lợi ích cho sức khỏe.', 'Một ly cà phê buổi sáng giúp tỉnh người nhanh.'),
    ('E08', 'chat', 'Tên của bạn là gì?', 'Bạn tên gì?'),
    ('E09', 'narration', 'vậy mà Gia Long biến chính chỗ ấy thành nơi cả nước kéo về chầu.', 'vậy mà Gia Long lại lấy chính chỗ ấy làm nơi cả nước kéo về chầu.'),
    ('E11', 'doc', 'Anh ấy rất khéo trong quan hệ với khách hàng.', 'Anh ấy khéo chiều khách.'),
    ('E12', 'narration', 'xin vào học trường Thuộc địa với tư cách thực tập sinh.', 'xin vào trường Thuộc địa học làm thực tập sinh.'),
    ('E13', 'chat', 'Nút Edit trên màn hình Research sử dụng endpoint này.', 'Nút Edit trên màn hình Research dùng chính endpoint này.'),
    ('F02', 'narration', 'Có lẽ có thể phần nào là do', 'Có lẽ phần lớn là vì'),
    ('F03', 'narration', 'nhiều khả năng là do', 'tôi nghĩ phần lớn là vì'),
    ('F05', 'doc', 'Hãy cùng khám phá những lợi ích tuyệt vời này nhé!', 'Caffeine ngấm vào máu chỉ sau vài phút và rõ nhất sau khoảng một tiếng.'),
    ('F05', 'doc', 'Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách Redis lưu dữ liệu.', 'Redis lưu dữ liệu thường dùng trong bộ nhớ, nhờ đó hệ thống ít phải truy cập nguồn dữ liệu chậm hơn.'),
    ('F05', 'doc', 'Chắc chắn rồi! Trong thời đại 4.0 ngày nay, AI không chỉ là một công cụ mà còn là người bạn đồng hành.', 'Phòng tôi bắt đầu dùng AI từ tháng trước, chủ yếu để soạn email và tóm tắt biên bản họp.'),
    ('F05', 'narration', 'Video này chỉ chọn kể năm kinh đô, còn những nơi khác thì mời các bạn kể thêm ở phần bình luận.', 'Video này chỉ kể năm kinh đô, những nơi còn lại các bạn cứ kể thêm ở phần bình luận.'),
    ('F08', 'doc', 'Endpoint này lưu nội dung vào `research/notes.md`, đồng thời giữ bản cũ trong `.history/research/`.', 'Endpoint lưu nội dung vào `research/notes.md`, giữ bản cũ trong `.history/research/`, và mở lại stage research nếu stage ấy đã approve.'),
    ('G01', 'chat', 'Hỏi: một người bị Pháp truy nã, không đặt chân về được, làm sao dựng được tổ chức trong nước?', 'Mật thám Pháp săn lùng gắt nên ông không về nước được. Ông mở lớp ở Quảng Châu, đưa thanh niên trong nước sang học rồi cho về gây dựng cơ sở.'),
    ('G01', 'chat', 'Trả lời: bàn hội nghị do các nước lớn quyết. Liên Xô và Trung Quốc muốn hoà vì việc riêng của họ, đổi lại một lời hứa tổng tuyển cử năm 1956.', 'Liên Xô và Trung Quốc đều muốn yên chuyện để lo việc nhà mình, nên ép Việt Nam nhận chia đôi ở vĩ tuyến 17, kèm lời hứa hai năm sau sẽ bầu cử thống nhất.'),
    ('G01', 'chat', 'Bài học: lời hứa trên giấy không ai bảo đảm thì thành chiến tranh.', 'Điều rút ra: lời hứa không ai đứng ra bảo đảm thì sớm muộn cũng thành chiến tranh.'),
    ('G03', 'chat', 'Dàn ý tập 1 đã xong và đã qua hai lượt phản biện chéo (Grok và GPT), bạn duyệt giúp trước khi mình cho viết lời.', 'Dàn ý tập 1 xong rồi, Grok với GPT đã đọc chéo hai lượt. Bạn xem giúp, ổn thì mình cho viết lời.'),
    ('G03', 'chat', 'Kết quả đo được: probe `SUMMARY gate=1/1 screen=23/23 selection=18/18 intent-route=41/41`, `make test` MAKE=0 (50 package).', 'Mình chạy lại hết rồi: probe đủ 41/41, make test qua cả 50 package.'),
]

# Sentences reviewers kept as natural (r4-changes.md "kept on purpose", linguistics report §4.2).
KEEP = [
    ('narration', 'có những tảng đá nặng tới mấy tấn'),
    ('narration', 'lúc ấy họ đang sợ nhất điều gì'),
    ('narration', 'Các nhà khảo cổ thì dè dặt hơn'),
    ('narration', 'nên pháo đài này vẫn gắn với đường sông'),
    ('narration', 'nhưng đó là truyền thuyết'),
    ('narration', 'xa hơn Thăng Long gần bảy mươi cây số'),
    ('narration', 'nên triều đại chẳng được lâu bền'),
    ('narration', 'Nơi ông chọn là thành Đại La'),
    ('narration', 'sớm hơn lời hẹn hai ngày'),
    ('narration', 'Bên ngoài còn một vòng tường đất'),
    ('narration', 'Thăng Long ba lần bị giặc đốt phá'),
    ('narration', 'Thăng Long bị giặc ngoài chiếm ít nhất sáu lần'),
    ('narration', 'và được gọi là chúa'),
    ('narration', 'Trong một tờ chiếu khác'),
    ('narration', 'Rồi chiếu chê nhà Đinh với nhà Tiền Lê cứ ở yên một chỗ nên triều đại chẳng được lâu bền.'),
    ('narration', 'thủ đô của cả nước thống nhất'),
    ('narration', 'Ngược lại ở Thăng Long'),
    ('narration', 'Một người nói lúc đã thắng, một người nói lúc sắp chết.'),
    ('narration', 'có lẽ vì đường xa nên quân không kịp tới'),
    ('narration', 'Hà Nội là kinh đô'),
    ('narration', 'Ông trả lời một câu mà Toàn thư còn chép lại:'),
    ('narration', 'Hai quyển sách anh cho tôi thì tôi đã đọc xong một quyển.'),
    ('narration', 'Nam bị thầy phạt, còn chị được mẹ khen.'),
    ('narration', 'Tôi gặp một người lính ở cổng.'),
]


def selftest():
    def ids(register, text):
        return {f['id'] for f in scan_text(text, register)}
    rows, caught_id, caught_any, fp_good = {}, 0, 0, 0
    fires = {}
    for pid, reg, bad, good in SELFTEST:
        r = rows.setdefault(pid, [0, 0, 0, 0])
        hb, hg = ids(reg, bad), ids(reg, good)
        r[0] += 1
        r[1] += pid in hb
        r[2] += bool(hb)
        r[3] += bool(hg)
        caught_id += pid in hb
        caught_any += bool(hb)
        fp_good += bool(hg)
        for x in hg:
            fires.setdefault(x, []).append(good)
    fp_keep = 0
    for reg, text in KEEP:
        h = ids(reg, text)
        fp_keep += bool(h)
        for x in h:
            fires.setdefault(x, []).append(text)
    n, k = len(SELFTEST), len(KEEP)
    print(f"{'id':5} {'pairs':>5} {'hit(id)':>8} {'hit(any)':>8} {'good flagged':>12}")
    for pid in sorted(rows):
        a, b, c, d = rows[pid]
        print(f'{pid:5} {a:5d} {b:8d} {c:8d} {d:12d}')
    print(f'\nrecall on bad, expected id: {caught_id}/{n} = {caught_id / n:.2f}')
    print(f'recall on bad, any cue:     {caught_any}/{n} = {caught_any / n:.2f}')
    total_fp = fp_good + fp_keep
    print(f'false positives on natural: {total_fp}/{n + k} = {total_fp / (n + k):.2f} '
          f'(rewritten good {fp_good}/{n}, reviewer-kept {fp_keep}/{k})')
    if fires:
        print('\npatterns that fired on natural sentences:')
        for pid in sorted(fires):
            print(f'  {pid}: ' + ' | '.join(s[:70] for s in fires[pid]))
    print('\nDensity ids (A07n, B01n, B08n, B09n, C01n, F01n) need a paragraph and are not exercised by single sentences.')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('path', nargs='?', help='text file, or - for stdin')
    ap.add_argument('--register', choices=sorted(REGISTER_OFF), default='narration')
    ap.add_argument('--json', action='store_true', help='print findings as JSON')
    ap.add_argument('--selftest', action='store_true', help='recall / false-positive table on the embedded pairs')
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    if a.path:
        text = sys.stdin.read() if a.path == '-' else Path(a.path).read_text()
        units = units_from_text(text)
    else:
        ap.print_usage()
        return 0
    findings = scan_units(units, a.register)
    if a.json:
        json.dump({'register': a.register, 'findings': findings}, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        print_plain(findings)
    return 0


if __name__ == '__main__':
    main()
    sys.exit(0)
