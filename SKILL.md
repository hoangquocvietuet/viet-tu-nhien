---
name: viet-tu-nhien
description: "Write and rewrite Vietnamese that sounds native, not English translated word by word (văn dịch, câu Tây). Use for ANY Vietnamese output, even when nobody asks: chat replies, status reports, plans and questions to a Vietnamese-speaking user, docs, READMEs, commit or PR text, emails and letters, UI strings, product and marketing copy, social posts and captions, titles, narration and voice-over scripts, and every translation into Vietnamese. Use it before sending a Vietnamese reply, and always when someone says the text 'nghe như dịch', 'giống dịch English', 'văn máy', 'không tự nhiên', 'thiếu tự nhiên', 'câu Tây', 'đọc cứng', or rejects a draft's wording. Gives a retell workflow, the patterns that make Vietnamese sound translated with real before/after pairs, an over-correction guard, a triage scanner (scripts/viet_scan.py) and a local RAG over references and native corpus (rag/)."
---

# viet-tu-nhien

Native readers reject drafts, and agents' own chat replies, that sound translated. Two real complaints from a native reviewer (Oct 2026): "viết văn tự nhiên hơn. lại giống dịch English one by word rồi" (about an agent's plan reply), "văn giờ vẫn mang phong cách dịch từ English sang Vietnamese" (same day, about a status reply). On one narration script a calque pass made 74 edits after two listening reviews had passed it; listening reviewers do not catch calques, and neither does a model reading its own text. Quotes below marked "reviewer" come from that native reader; `docs/use-cases.md` maps each kind of text to a register and the commands to run.

## Core idea: retell, do not translate

English-shaped structure leaks even when every word is Vietnamese. "Cái gì giữ một kinh đô" has no English word in it, yet it is "What keeps a capital" with Vietnamese words dropped into the slots. The skeleton (abstract subject, article, pronoun "it", passive, "of" chain, "with", "when"-clause) is what the ear catches.

So compose in Vietnamese from the facts:

1. Get the facts as a short list: who, did what, to whom, when, where, what followed.
2. Ask how a Vietnamese person would tell this to the person in front of him, then say that. Concrete doer first, then the verb.
3. Never polish a Vietnamese draft word by word when its skeleton is English. Word swaps keep the skeleton ("nên là" → "nên"); retell the paragraph from its fact list instead.
4. If you think in English, think in facts, not in sentences. An English sentence in your head becomes the Vietnamese sentence's skeleton.
5. Big ideas have Vietnamese names already: cứu nước, mất nước, tìm đường, chưa biết ngả về đâu, rơi vào bế tắc, giành độc lập. Use them; do not coin a phrase for an English concept because the set phrase feels like a textbook. The coinage is what sounds translated ("làm sao cho một thuộc địa thoát ra" → "đường nào để cứu nước"). Slogans are praise and verdicts ("mốc son chói lọi"), not plain names. Table: `references/cach-goi.md`.

**English sources** (research notes, logs, READMEs, English docs): read the English, close it, and write a Vietnamese fact list in your own words, not sentence by sentence. Write the Vietnamese from that list and go back to the English only to check facts. The bullet order of the source is not the order of the telling. In an A/B eval (Oct 2026) both writers, with and without this skill, turned *useful to France in relation to his compatriots* into "có ích cho nước Pháp trong quan hệ với đồng bào"; the baseline turned *bring them the benefits of instruction* into "đem lại cho họ những lợi ích của việc học", where the writer with the skill said "đem sự học ấy về cho họ". Most leaks in that eval sat where a sentence was carried over from the English.

## Workflow

### 1. Register gate

Decide the register before writing; the same structure is natural in one and wrong in another.

| register | what it is | keep | cut |
|---|---|---|---|
| `narration` | Spoken script heard once (voice-over, video, podcast, presentation) | văn nói, the narrator's voice, Hán-Việt names and terms of art, quotes word for word | essay connectives, signposting, labels, anything that only works on paper |
| `chat` | An agent's reply, status report, plan, or question to the user | the user's own words for tools ("render", "approve", "commit"), the pronouns the user uses ("mình/bạn", "anh/em"), short full sentences | bold label lists, "Dưới đây là", passive status lines, headline-then-restatement |
| `doc` | README, notes, reports, captions, descriptions | headings, some nominalisation for terms, an occasional "tuy nhiên" | English idioms, "của" chains, "nó" for things |
| `formal` | Letters, official or legal text | Hán-Việt, passive where the law hides the agent | calqued frames ("đóng vai trò", "có số phận") |

For text that goes to TTS, also write out numbers, units and symbols the way the narrator says them.

### 2. Lock before you rewrite

Write down what must survive: facts, numbers, dates, names, quotes (verbatim), hedges ("có lẽ", "tôi đoán", "theo tôi"), negation, scope ("trong năm kinh đô ta kể"), and attribution (who said or recorded it). A smoother sentence that drops "tôi đoán" has turned an inference into a fact; that is worse than a calque.

### 2b. Mạch ý before the draft

Writing one sentence per fact and then adding connectives gives a paragraph that is glued, not linked; the reviewer, on such a set: "tôi vẫn chưa hài lòng lắm. cảm giác content chưa liên kết". Before drafting a paragraph (narration, or any reply longer than three sentences), write down in a scratch note:

1. **Sợi chỉ**: one sentence saying what the paragraph moves the listener from and to ("Người muốn học để về giúp đồng bào → nước Pháp đóng cửa trường bằng một thủ tục → Người học bằng con đường khác").
2. **Chuỗi câu hỏi**: for each planned sentence, the question the previous sentence leaves in the listener's head, and how this sentence answers it. A fact that answers no question either moves to where it does or goes. Example: "Người vẫn chỉ là phụ bếp làm thuê" → (vậy làm sao xem cho tận tường?) → "Muốn xem cho tận tường thì phải được học, nên… Người viết đơn" → (trường trả lời sao?) → "Thư đi chừng một tháng thì có hồi âm, mà hồi âm là lời từ chối" → (vì sao?) → "Lý do nằm ở thủ tục:…".
3. **Gọi lại**: one detail the listener already holds from an earlier chapter or paragraph, brought back where it gives the new fact its meaning (the Sài Gòn promise "xem họ làm thế nào rồi về giúp đồng bào" is what makes the Marseille letter matter).

Narrator inferences that the chain needs ("Muốn xem cho tận tường thì phải được học") are allowed only as the narrator's reading and go to the fact-check marked as inference. The connective then follows from the relation in the chain; pick it from `references/connectives.md`, never add it afterwards to glue two facts.

### 3. Draft

- Doer and verb: "Toàn thư chép lại câu ông nói", not "Câu ông nói được Toàn thư ghi lại".
- Topic first when the listener already holds it, then the comment: "Hoa Lư thì…", "Tới năm 1285…".
- Repeat the noun or use "ấy" instead of "nó"; drop the subject while the actor stays the same.
- Link sentences by their real relation: nhưng, nên, thế là, mà, thì, rồi, còn.
- One idea per sentence; split where the topic changes, not by a length quota.
- Glosses go before or after a full clause, never between subject and verb.
- From an English source, write from your Vietnamese fact list with the English closed (§ Core idea, English sources); reopen it only to check a fact.

### 3b. Reference pack, then rewrite

Order: viết nháp → RAG tham khảo → viết lại → review. Do not load every reference file while writing; fetch only what each draft sentence needs (setup: `docs/rag-setup.md`):

```bash
python3 ~/.agents/skills/viet-tu-nhien/rag/viet_rag.py ref draft.md --register narration   # per-sentence pack
python3 ~/.agents/skills/viet-tu-nhien/rag/viet_rag.py search "cứu nước" -k 5               # one lookup
python3 ~/.agents/skills/viet-tu-nhien/rag/build.py --stats                                  # rebuild after any reference or corpus change
```

The pack lists, under each draft sentence, the scanner patterns that fire, lines native reviewers rejected, real before→after pairs, the Vietnamese name for the idea (`cach-goi.md`), connectives and native excerpts. Rewrite the draft with the pack open: take the joins and names, never copy an excerpt's facts or period voice. Then go on to step 4. Retrieval is hybrid by default: SQLite FTS5 keywords fused with a local embedding model (`gte-multilingual-base`, `rag/README.md`), so a draft that says "giải phóng đất nước" still reaches the "cứu nước" row; `--mode keyword` skips the model, and the header says when the vector layer is missing. Plain fact sentences still pull units that share a name or number; ignore those.

### 4. Scanner: triage only

```bash
python3 ~/.agents/skills/viet-tu-nhien/scripts/viet_scan.py draft.md --register chat
printf '%s' "$TEXT" | python3 ~/.agents/skills/viet-tu-nhien/scripts/viet_scan.py - --register doc --json
```

Each cue names a pattern id from `references/patterns.md` and the sentence. Reread each flagged sentence aloud; keep it if a Vietnamese speaker would say it. The scanner sees surface shapes only: an agent's rewritten plan (`references/pairs.md` § G) raises one cue, and the reviewer still judged that day's prose translated. Zero cues proves nothing.

### 5. Read-aloud audit

Review in small pieces (reviewer rule, Oct 2026: "chia nhỏ từng đoạn review chứ đừng review cả cục"). One paragraph at a time, sentence by sentence, with the last sentence before it for context; never a whole script or a long reply in one pass. A long text gets several reviewers, one chunk each. One sample narration paragraph passed its writer's own audit and the scanner with zero cues; read sentence by sentence it still had three calques and a label sentence.

Read every sentence as if saying it to the person you write for, and answer per sentence:

- **Ai làm gì?** Who acts, and on what? If the story needs a doer and the sentence has none (passive, "việc…", abstract subject), name it.
- **Đề là gì?** What is the topic the listener is holding? Does the sentence start from it?
- **Đại từ trỏ về đâu?** For every nó, ông, họ, ấy, đó: can the listener point at exactly one thing?
- **Nói một hơi được không?** Each comma group in one breath; no gloss wedged before the verb.
- **Người Việt có nói đúng câu này không?** In these words, to someone in front of him? Back-translate it in your head: if it becomes a fluent English sentence word for word, the skeleton is English.
- **Nghe ra có sai nghĩa đen không?** "Ruộng ấy lên xuống theo thủy triều": the field does not move.
- **Nghe xong có biết nó là gì không?** A label noun standing in for content ("một câu thủ tục", "một tờ giấy hành chính", "câu trả lời ấy", "lý do ấy") leaves the listener asking what it said. Put the content right there: "nhận về một lời từ chối theo đúng thủ tục: đơn như thế phải đi qua Toàn quyền Đông Dương". The reviewer, on "và nhận về một câu thủ tục": "câu thủ tục là gì? đang hơi cụt ngủn".
- **Ý lớn này người Việt gọi là gì?** For every abstract idea in the sentence (goal, way, failure, rule, turning point), is it the name Vietnamese already uses (`references/cach-goi.md`) or a phrase built from an English concept ("một thuộc địa thoát ra", "một sợi chỉ chung", "lối đi tiếp")?

### 5b. Read the paragraph whole (second layer)

A sentence-by-sentence pass removes calques but cannot see flow. After it, a different agent reads the whole paragraph aloud once, with the last sentence before it and the first after, and checks only § Mạch kể and step 2b: for every sentence, what question did the sentence before leave, and does this one answer it (a sentence that answers nothing is marked **rời** with the fact it carries, and either moves or goes); does the paragraph bring back something the listener already holds; at every full stop, is the relation to the previous sentence said (contrast needs "Nhưng"/"Vậy mà" at the start); is the passage of time clear; are there three or more short stand-alone sentences in a row; does any join rely on a bare "Rồi"/"Và"; is there a label where content should be. This reader may merge and reorder sentences; every rewrite goes back through the patterns and the scanner, and facts are checked again (step 7).

### Who judges

The reader does: the user you write for, or a native speaker. A model's naturalness score is not proof. In the same eval a GPT-family judge rated the baseline higher and proposed rewrites that are themselves translated or bookish: "Mình bổ sung 3 bài test, cả ba đều đạt", "sử dụng endpoint này", "đã được duyệt sẽ được mở lại", "Theo cách tường thuật phổ biến". That is one observation, not a measured rate, but it is enough to set the rule: a reviewer agent must quote the exact phrase and name the English structure behind it (`patterns.md` id or the English words), and its own proposed rewrite must pass the same patterns and the scanner.

### 6. Over-correction guard

Fewer flags is not more natural. Before changing a flagged sentence, check § Do not over-correct below and the "Giữ nguyên" list in `references/pairs.md`. "No change" is a valid answer: say which flagged sentences you kept and why.

### 7. Equivalence check

Compare every changed sentence with the locked list from step 2: same facts and numbers, same quote wording, same hedge strength, same negation, same scope, same speaker. For factual texts (history, news, docs), send reworded sentences back through a fact-check; for a large rewrite, have an agent of a different model family check equivalence.

## The patterns that do the most damage

Ranked by how often they appeared in real rewrites and how badly they give the text away. Ids point to `references/patterns.md`; more pairs in `references/pairs.md`.

1. **Abstract or nominalised subject** (A01, A03). English makes a wh-clause or "the thing that" the subject. `Vậy không phải bức tường thì rốt cuộc cái gì giữ được một kinh đô?` → `Vậy không phải nhờ bức tường thì rốt cuộc kinh đô đứng được lâu là nhờ đâu?`
2. **"một" as an English article** (B01, B02). It is a numeral. `nên quân Nguyên vào chỉ thấy một tòa thành không có lương.` → `nên quân Nguyên vào tới nơi chỉ thấy thành không, kho chẳng có lương.`
3. **"nó" for things and places** (B05). Repeat the noun, use "ấy", or drop it. `dù tới giờ nó vẫn còn đứng đó.` → `dù tới giờ tường vẫn còn đứng đó.`
4. **Passive "được/bị … (bởi)" hiding the doer** (C01, B12, C03). `Câu ông nói được Toàn thư ghi lại thế này:` → `Toàn thư chép lại câu ông nói thế này:`
5. **"việc/sự/cuộc + V" and light verbs** (D01, D02): tiến hành, thực hiện, đưa ra một quyết định, trải qua cả một cuộc. `tiện cho việc làm ăn.` → `tiện đường làm ăn.`; `Ông vừa trải qua cả một cuộc nội chiến` → `Nội chiến vừa mới dứt`
6. **English frames and idioms** (E01): mở ra chương mới, đóng vai trò, số phận khác, kẻ thù đến từ, đặt lên cùng một. `ta thấy hai kiểu kinh đô có số phận khác hẳn nhau.` → `thì thấy hai kiểu kinh đô đi hai ngả khác hẳn nhau.`
7. **"của" chains and "của" before names** (B09, B10). `chọn Huế làm kinh đô của nhà Nguyễn.` → `chọn Huế làm kinh đô nhà Nguyễn.`; `xã Đông Anh của Hà Nội` → `xã Đông Anh ở Hà Nội`
8. **English causatives "X khiến/làm cho/dẫn tới Y"** (E02). Tell the event, then what followed. `và chính tờ thứ hai dẫn tới một kinh đô mới.` → `mà chính tờ thứ hai mới sinh chuyện dựng kinh đô mới.`
9. **"khi / trước khi / sau khi" clause order** (A09). `Một người nói sau khi thắng,` → `Một người nói lúc đã thắng,`; `Rồi khi quân tới Tam Điệp, ông gọi` → `Tới Tam Điệp, ông gọi`
10. **English comparatives** (E04). `lâu hơn Tây Đô rất nhiều.` → `Tây Đô làm sao bì được.`; `Tây Đô khó bị đánh hơn,` → `Tây Đô dễ giữ hơn,`
11. **"với" = with** (B11). `là Cổ Loa với ba vòng lũy đất,` → `là Cổ Loa có ba vòng lũy đất,`
12. **Glosses wedged between subject and verb** (A07). `Lúc ấy thái thú, tức viên quan nhà Hán cai cả một quận, cùng các quan Hán khác chỉ còn…` → `Trong khi đó các quan Hán ở đây, kể cả những thái thú cai cả một quận, chỉ còn…`
13. **"là + adjective"** (E03). Adjectives are predicates. `Điều này là quan trọng đối với cuộc chiến.` → `Điều này quan trọng với cuộc chiến.`
14. **Hedge stacks and translated hedges** (F02, F03). `Có lẽ có thể phần nào là do…` → `Có lẽ phần lớn là vì…`; `nhiều khả năng là do` → `tôi nghĩ phần lớn là vì`
15. **Essay connectives in speech** (F01): tuy nhiên, do đó, bên cạnh đó, ngoài ra, hơn nữa. `Bên cạnh đó… Ngoài ra… Hơn nữa…` → `Nhưng…`, `Cùng lúc ấy…`, or nothing when there is no real relation.

Also common: summary frames that announce instead of telling (A08), "và đó là" / ", nơi sau này" tails (A10), dictionary words a speaker would not pick (E10: `cách đọc của Taylor` → `nhận xét của Taylor`), and classical phrases left in their literal shape (D03: `Chỉ đủ tự giữ` → `chỉ còn biết lo giữ mình`).

## Mạch kể: join sentences into a story

Removing every calque can still leave a dead paragraph: a row of short sentences, each one fact, joined by "Rồi". On one narration paragraph the sentence-level reviewer split every "và" sentence (A12) and the result read like a report; the reviewer: "vẫn chưa ổn lắm". Nobody had read the paragraph whole.

- Move through time the way people tell it, counting from the event the listener already holds: "Ở đất Pháp được hơn hai tháng, Người ngồi viết một lá thư.", "Thư đi chừng một tháng thì có hồi âm.", "Sang đầu năm 1912,…". A new date stamp for every event is a timeline, not a story.
- Each sentence picks up what the last one left open: a letter sent, then its answer; a refusal, then why.
- Say the relation the story turns on, including the irony: "vậy mà", "thế mà", "mà", "nên", "thì". Not essay connectives (F01), not "khiến/dẫn đến" (E02).
- The join between two sentences needs its word too, not only the join inside one. When a sentence sets up what the listener expects and the next goes against it, open the next with "Nhưng" or "Vậy mà"; a bare full stop drops the turn. The reviewer on `Nước Pháp vẫn lấy ba chữ Tự do, Bình đẳng, Bác ái làm khẩu hiệu. Người gõ cửa, nhưng trường không nhận:…`: "2 câu này chưa có từ liên kết… Thêm 1 từ nhưng nữa là hợp". Fix: `…làm khẩu hiệu. Nhưng Người gõ cửa thì trường không nhận, vì theo thủ tục, đơn như thế phải gửi qua Toàn quyền Đông Dương.` Move the inner "nhưng" to the sentence start and join the rest with "thì"; two "nhưng" in a row is worse.
- Vary the joining words (reviewer: "đa dạng từ ngữ hơn", "nhiều từ nối hơn, từ về mở rộng ý chẳng hạn"). Pick the relation first (thêm ý, nói rõ, thời gian, nhân quả, đảo ý, điều kiện, chốt), then the word: `references/connectives.md` lists each group with examples. Contrast alone has many: nhưng, vậy mà, thế mà, ấy thế mà, có điều, còn, "lại" inside the verb, "rốt cuộc"; adding has lại còn, đã vậy, chưa hết, chưa kể, thêm nữa, đến cả, huống hồ. Do not reuse the same one within about three sentences. "Nào ngờ", "không ngờ", "chẳng ngờ" say someone expected otherwise: use them only when a source records that expectation.
- Vary length: a long sentence that carries a sequence, then a short one that lands ("Trường không nhận"). Splitting every comma chain is as wrong as keeping all of them.
- Content, not labels (A14).
- No stock transitions from school essays or "how to write" lists: "Nếu coi A là bề nổi của tảng băng chìm thì B…", "Minh chứng rõ nét nhất cho điều này…", "Không dừng lại ở đó…", "Khép lại vấn đề…", "Bạn đã bao giờ…?". The reviewer once pasted such a list as a direction; the idea (chuyển ý, lời dẫn) is right, the phrases are AI tells.

Pair (a history narration paragraph about Nguyễn Tất Thành in Marseille, 1911; v3 after the calque pass → v4, the direction the reviewer approved):

- `Ngày 15/9/1911, ở Marseille, Người viết tay một lá thư… Thư viết bằng tiếng Pháp, có đoạn Người kể về mình:… Nước Pháp vẫn lấy ba chữ Tự do, Bình đẳng, Bác ái làm khẩu hiệu. Người gõ cửa, nhưng trường không nhận,…`
- → `Ở đất Pháp được hơn hai tháng, Người ngồi viết một lá thư. Thư đề ngày 15/9/1911, viết tay bằng tiếng Pháp,… Thư đi chừng một tháng thì có hồi âm. Trường không nhận, vì đơn xin học như thế phải nộp qua Toàn quyền Đông Dương, tức là qua chính bộ máy đang cai trị quê nhà. Nước Pháp vẫn lấy ba chữ Tự do, Bình đẳng, Bác ái làm khẩu hiệu, vậy mà muốn vào học trường của họ, Người lại phải đi xin chính quyền thuộc địa.`

Next step, linked by question chain and call-back (step 2b; approved as direction 2026-10-27 after "content chưa liên kết"; the two narrator inferences still need a fact-check):

- `Hồi ở Sài Gòn, Người từng nói muốn sang xem nước Pháp và các nước khác làm thế nào, rồi về giúp đồng bào. Tới Marseille đầu tháng 7/1911, Người vẫn chỉ là phụ bếp làm thuê cho hãng Năm Sao. Muốn xem cho tận tường thì phải được học, nên ở đất Pháp được hơn hai tháng, Người viết tay một lá đơn bằng tiếng Pháp, gửi thẳng lên Tổng thống và Bộ trưởng Thuộc địa, xin vào trường Thuộc địa. Trong đơn, Người kể thật về mình: không có gì để sống, và khao khát được học. Thư đi chừng một tháng thì có hồi âm, mà hồi âm là lời từ chối. Lý do nằm ở thủ tục: đơn như thế phải qua Toàn quyền Đông Dương, tức là qua chính bộ máy đang cai trị quê nhà. Thành ra người dân thuộc địa muốn học cái hay của nước Pháp thì trước hết phải xin phép kẻ đang cai trị mình. Không vào được trường, Người vẫn làm thuê như cũ. Có dạo tàu nằm sửa, Người theo chủ tàu về Sainte-Adresse làm vườn, rồi sang đầu năm 1912 lại xuống một tàu chở hàng của hãng Năm Sao. Lớp học không mở cửa, thì những bến cảng sẽ thành chỗ Người học.` ("Nói cách khác" in the first version was swapped for "Thành ra": the essay-only list bans it.)

Native models of telling this period: `references/pairs.md` § Mạch kể, verbatim excerpts from Trần Dân Tiên and T. Lan with the device each one uses.

## Chat replies

The user reads agents' replies with the same ear. A reply is a message from a colleague, not a slide.

- No bold label lists and no "Hỏi:", "Trả lời:", "Kết quả:", "Bài học:" lines. Write the sentence the label stands for.
- No "Dưới đây là", "Sau đây là", "Hãy cùng", "Hy vọng thông tin này…", "Nếu bạn cần thêm…".
- No headline followed by a sentence that says the headline again.
- Status lines say who did what: not "đã qua hai lượt phản biện chéo", "Kết quả đo được là…", "Phản biện khiến mình sửa…", "sẽ được kiểm lại".
- Ask questions the way a person asks: "Bạn thấy sao?", "ổn thì mình làm tiếp", not "Giữ, hay né?".
- Keep the user's own technical words (render, approve, commit, cache) as the user writes them; do not translate them into Hán-Việt. Mixing them into Vietnamese sentences is fine.
- Address the user with the pronouns the user uses ("mình/bạn" in the pairs below). Do not switch to "anh/em" unprompted; a baseline writer in the eval answered a "mình/bạn" log with "Xong rồi anh nhé", "Em thêm màn hình Research".

Pairs. "Real" = both sides from one agent session (Oct 2026: the agent's first reply, then its rewrite after the reviewer's complaint; the rewrite is a direction, not an approved model). "Bad real" = the left side is a real reply the reviewer rejected; the right side was written for this skill.

| | bad | natural |
|---|---|---|
| status, bad real | Dàn ý tập 1 đã xong và đã qua hai lượt phản biện chéo (Grok và GPT), bạn duyệt giúp trước khi mình cho viết lời. | Dàn ý tập 1 xong rồi, Grok với GPT đã đọc chéo hai lượt. Bạn xem giúp, ổn thì mình cho viết lời. |
| status, bad real | Phản biện khiến mình sửa những chỗ này so với bản đầu: | Grok và GPT đọc chéo xong, mình sửa mấy chỗ này so với bản đầu: |
| status, bad real | Kết quả đo được: probe `SUMMARY gate=1/1 screen=23/23 …`, `make test` MAKE=0 (50 package) | Mình chạy lại hết rồi: probe đủ 41/41, `make test` qua cả 50 package. |
| status, bad real | Ngày tháng và chi tiết dưới đây sẽ được kiểm lại ở bước research. | Ngày tháng với chi tiết thì mình sẽ kiểm lại ở bước research. |
| plan, real | Hỏi: một người bị Pháp truy nã, không đặt chân về được, làm sao dựng được tổ chức trong nước? | Mật thám Pháp săn lùng gắt nên Người không về nước được. Người mở lớp ở Quảng Châu, đưa thanh niên trong nước sang học rồi cho về gây dựng cơ sở. |
| plan, real | Mục tiêu (độc lập, thống nhất) giữ nguyên, còn cách đi thì mỗi tập một kiểu. | Nghĩa là độc lập và thống nhất thì giữ chắc, còn cách đi thì tùy lúc mà đổi. |
| plan, real | Cả chuỗi có chung một sợi chỉ là câu Bác dặn cụ Huỳnh Thúc Kháng năm 1946 | Cả chuỗi xoay quanh câu Bác nói năm 1946 |
| question, real | Mình nghĩ có những chuyện này thì phim mới sâu, và tất cả đều đã có trong sử chính thống. Giữ, hay né? | Mình muốn giữ vì có những chuyện này phim mới sâu, và sử chính thống đều đã nhắc tới. Bạn thấy sao? |
| question, real | Bạn chốt giúp ba điểm: 1. Dàn ý này được chưa? Tập nào muốn đổi câu hỏi? | Bạn xem giúp: 1. Dàn ý được chưa, có tập nào muốn đổi không? |
| opener (minh họa) | Dưới đây là kế hoạch chi tiết cho việc triển khai tính năng mới: | Mình định làm ba bước: |

## Do not over-correct

Every pattern above has native uses. Keep:

- **bị / được** with their own meaning: adversity and benefit ("Thăng Long bị giặc ngoài chiếm ít nhất sáu lần", "chị được mẹ khen"), and "được gọi là". Reviewers kept these.
- **Classifiers** (một tờ chiếu, ba bức tường, chiếc thuyền). Never strip a correct classifier to "fix" an article.
- **"một" that counts, introduces, or contrasts**: "còn một vòng tường đất", "Trong một tờ chiếu khác", "Một người nói…, một người nói…", "Tôi gặp một người lính ở cổng".
- **"là" in identity sentences**: "Hà Nội là kinh đô", "Nơi ông chọn là thành Đại La".
- **"của" where possession is the point**: "thủ đô của cả nước thống nhất", "lời của ông".
- **Hán-Việt terms of art**: triều đình, kinh đô, khởi công, thắng địa (with a plain gloss once).
- **Formal register where it was chosen**, old quotes, a deliberately bookish lead-in.
- **"thì", topic–comment**: "Hai quyển sách anh cho tôi thì tôi đã đọc xong một quyển."
- **Hedges and scope**: never drop "tôi đoán", "có lẽ", "trong mấy kinh đô ta kể" to make a sentence smoother.
- **Sentences joined by "và", "mà", a comma**, when one event leads into the next. Do not split a paragraph into one-fact sentences (§ Mạch kể).

Natural is not casual. A history narrator still sounds composed; a reply to the user is friendly but not slangy. Do not add emoji, filler particles, or invented feelings to "sound human".

## Files

- `references/patterns.md`: the full catalogue (66 patterns, A–G), each with English source, real pair, why it sounds foreign, detectability and source. Read it when the scanner names an id, when reviewing a whole script, or when briefing another agent on calques.
- `references/pairs.md`: all real before → after pairs with file references, grouped by id; the "Giữ nguyên" list; rewrites that went too far. Use it for few-shot examples in a writer or calque-pass prompt, and before changing a sentence the scanner flagged.
- `references/connectives.md`: joining words grouped by relation (thêm ý, nói rõ, thời gian, nhân quả, đảo ý, điều kiện, chốt), with examples and the essay-only list. Read it when writing or flow-reading narration (§ Mạch kể, step 5b).
- `references/cach-goi.md`: big ideas (independence, colonial rule, the way forward, dead end, labour, turning point) with the wordings Vietnamese-original sources use, ids traceable to `references/corpus/`, and the slogan list. Read it before writing narration about history or politics.
- `references/corpus/`: verbatim excerpts with URLs, Oct 2026: `corpus-sach-su.md` (popular history articles), `corpus-loi-binh.md` (VOV/VTV narration), `corpus-but-ky.md` (Tam Lang, Vũ Trọng Phụng, Tô Hoài), `mach-ke-corpus.md` (Trần Dân Tiên, T. Lan), `corpus-luyen-van.*` (Nguyễn Hiến Lê, *Luyện văn* I–III: 34 style rules in his words, e.g. "Khi Việt ngữ đã sẵn có một cách để phô diễn đúng tư tưởng thì đừng nên mượn cách phô diễn của ngoại quốc"), `corpus-loi-binh-video.*` (YouTube narration from 7 channels, auto-captions with punctuation added). The `.jsonl` files are the RAG input format. Do not load these whole; query them through `rag/`. Adding a source: `docs/rag-setup.md` § Thêm nguồn.
- `rag/`: `build.py` (SQLite FTS5 index of every reference, corpus record and flagged line, plus vectors in `viet_vec.db`; rebuilds itself when a source is newer and re-embeds only changed units; a full build takes ~45 s and 1.1 GB RAM; `--stats`), `vec.py` (embedding model, 340 MB in `models/`, a download), `viet_rag.py` (`search`, `ref` per-sentence pack, `--mode keyword|vector|hybrid`, `--selftest`), `README.md`. Drop a new `references/corpus/<slice>.jsonl` (fields id, kind, text, source, url, register, tags, note) and it is indexed on the next run.
- `evals/user-flagged.md`: the lines native reviewers rejected, with facts and context. After any change to this skill, have a fresh agent write those lines from the facts and show a native reader old and new side by side; log the verdict there.
- `scripts/viet_scan.py`: triage scanner (stdlib Python, never rewrites, exit 0). `--register narration|chat|doc`, `--json`, `--selftest`. The self-test runs the embedded pairs: recall on the bad side and false positives on the natural side and the reviewer-kept sentences. The regexes were written with these pairs in view, so read its numbers as a regression check, not as accuracy on new text.
- `docs/use-cases.md`: which register, which checks and which commands for each kind of text. `docs/rag-setup.md`: install, build, test and extend the RAG.
