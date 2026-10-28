# Catalogue: English-shaped Vietnamese

Merged from three research reports (internal calque pass, linguistics sources, existing Vietnamese humanizer skills), deduplicated. Ids match `scripts/viet_scan.py`; an id ending in `n` in the scanner is the paragraph-density version of the same pattern. All pairs here are real unless marked **(minh họa)**; the full pair list with file references is `pairs.md`.

Read a row as "this shape often comes from English", never as "this word is banned". Every row has native uses; § Giữ nguyên in `pairs.md` lists sentences reviewers kept.

**Detect** column: `regex` = the scanner flags it with fair precision; `regex·n` = only by density in a paragraph; `heur.` = the scanner gives a weak cue, judge by ear; `human` = no scanner rule, only the read-aloud audit finds it.

## Contents

- [A. Khung câu và chủ thể](#a-khung-câu-và-chủ-thể) A01–A13
- [B. Hư từ dịch từng chữ](#b-hư-từ-dịch-từng-chữ) B01–B16
- [C. Bị động và người làm bị giấu](#c-bị-động-và-người-làm-bị-giấu) C01–C05
- [D. Danh hóa và động từ đệm](#d-danh-hóa-và-động-từ-đệm) D01–D06
- [E. Khung, thành ngữ, logic kiểu Anh](#e-khung-thành-ngữ-logic-kiểu-anh) E01–E13
- [F. Liên từ, rào đón, lời dẫn](#f-liên-từ-rào-đón-lời-dẫn) F01–F08
- [G. Trả lời chat](#g-trả-lời-chat) G01–G05
- [Sources](#sources)

## A. Khung câu và chủ thể

| id | tên | English source | bad | natural | why it sounds foreign | detect | source |
|---|---|---|---|---|---|---|---|
| A01 | Chủ thể trừu tượng, câu hỏi vòng | *What keeps…? / What the sources record…* | Vậy không phải bức tường thì rốt cuộc cái gì giữ được một kinh đô? | Vậy không phải nhờ bức tường thì rốt cuộc kinh đô đứng được lâu là nhờ đâu? | English lets a wh-clause be the subject; Vietnamese puts the concrete thing first and asks "nhờ đâu / vì sao". | regex | r4 c01p03; title c09 "Cái gì giữ một kinh đô" → "Không phải nhờ bức tường"; WP §1 "Những gì sử sách còn ghi…" |
| A02 | Danh từ mang mệnh đề làm chủ ngữ | *The capital he chose was X* | Kinh đô ông chọn là Hoa Lư, | Ông chọn đất Hoa Lư làm kinh đô, | Packs the action into a noun phrase, then a copula; the next sentence starts with "Ông" again. Native when it is a deliberate topic ("Nơi ông chọn là thành Đại La" was kept). | human | r4 c04p01 |
| A03 | Câu chẻ "Thứ/Cái … là" | *The thing that is real is… / What they kept was…* | rút khỏi thành, tôi thấy lời ấy khá khớp, cái họ giữ là dân với lương còn cái thành thì họ bỏ lại. | rút khỏi thành mới thấy lời ấy đúng thật, vì họ giữ lấy dân với lương còn thành thì bỏ lại. | Cleft copied from English; Vietnamese says the verb with its doer. | regex | r4 c06p03; r4 c03p03 "Thứ có thật là…" |
| A04 | Đề–thuyết bị ép thành "là thứ mà" | *X is the thing that I…* | Loại táo này là thứ mà tôi rất thích ăn. | Loại táo này tôi rất thích ăn. | Vietnamese is topic-prominent: topic, then comment; no relative clause needed. | regex | E5 (Nguyễn Văn Hiệp) |
| A05 | Câu tồn tại đảo | *There is X in Y / X exists in Y* | Không có mặt trời ở đây. | Ở đây không có nắng. | Vietnamese puts the place first as topic; "tồn tại" copies *exist*. | heur. | E1 (Cao Xuân Hạo); E5 "Ở Việt Nam có nhiều xe máy" |
| A06 | "mà" quan hệ thừa | *the person who/that I met* | Người mà tôi gặp hôm qua là nhà văn. | Người tôi gặp hôm qua là nhà văn. | The modifier clause follows the noun with no linker; "mà" everywhere echoes *who/that*. | heur. | E5 |
| A07 | Lời giải thích chen giữa chủ ngữ và động từ | appositive *X, i.e. Y, V…* | Lúc ấy thái thú, tức viên quan nhà Hán cai cả một quận, cùng các quan Hán khác chỉ còn… | Trong khi đó các quan Hán ở đây, kể cả những thái thú cai cả một quận, chỉ còn… | A listener loses the subject before the verb arrives; also glosses that only repeat a quote ("thế cô, tức là lẻ loi…"). | heur. (+ `tức là` density) | WP §1 |
| A08 | Câu tóm-rồi-kể, câu nhãn | *Each side relied on one thing. The Han… The sisters…* | Theo tôi thì trước khi đánh nhau, mỗi bên đã dựa vào một thứ. Nhà Hán dựa vào… Còn Hai Bà dựa vào… | Tính ra thì đến lúc hai bên giáp mặt, nhà Hán đã có gần hai năm lo đường sá, thuyền bè và lương thực… | An essay's topic sentence; a storyteller goes straight to the fact. | human | WP §1 |
| A09 | Mệnh đề thời gian, mục đích đặt kiểu Anh | *after/before/since/when…, To know…, …* | Một người nói sau khi thắng, | Một người nói lúc đã thắng, | "sau khi / trước khi / kể từ khi" and fronted "Khi…, / Để…," follow English clause order; speech says "lúc đã…", "từ lúc…", "Muốn… thì…", or tells in order. | heur. | r4 #9 (10 rows): c09p03, c04p04, c06p01, c06p05, c03p04, c02p02 |
| A10 | Đuôi câu kiểu Anh "và đó là", ", nơi sau này" | *and that was the first time; …, where later…* | Đó là cửa sông Hương thông ra biển, nơi sau này hạm đội Pháp kéo vào. | Đó là cửa sông Hương thông ra biển, về sau hạm đội Pháp kéo vào chính từ đây. | Relative tail hung on a place; Vietnamese starts a new clause ("thế là…", "về sau…"). | heur. | r4 c08p05, c06p01 |
| A11 | Lặp đại từ chủ ngữ mỗi câu | *He… He… He…* | Nhà vua bước vào thành. Ông ấy nhìn quanh. Ông ấy gọi quân lính. Ông ấy ra lệnh đóng cổng. **(minh họa)** | Nhà vua bước vào thành, nhìn quanh rồi gọi quân lính đóng cổng. **(minh họa)** | English needs a subject in every clause; Vietnamese drops it while the actor is unchanged. | regex | linguistics report P05; WP §1 "redundant subjects" |
| A12 | Chuỗi dấu phẩy nhịp văn viết | comma-chained clauses | Quân Hán tới với đường, thuyền và lương đã lo suốt gần hai năm, còn các Lạc tướng thì có lẽ… | Quân Hán kéo tới với đường sá, thuyền bè và lương thực đã lo gần hai năm. Chuyện thứ hai là các Lạc tướng có lẽ… | English packs relations into one sentence; spoken Vietnamese splits where the topic changes. | heur. | linguistics report P44, from the Hai Bà Trưng rounds |
| A13 | "kể từ khi/lúc" | *since* | Nếu file đã bị thay đổi kể từ lúc tải, endpoint trả về lỗi 409. | Nếu file đã đổi từ lúc được tải lên màn hình, endpoint trả 409 và không ghi gì. | "kể từ" carries *since* into chat and docs; speech says "từ lúc", "tính từ lúc". | heur. (info) | EV T3 (out-b → out-a); r4 c04p04 |
| A14 | Danh từ nhãn thay cho nội dung | *and got back a procedural answer* | Người gõ cửa nước Pháp của ba chữ Tự do, Bình đẳng, Bác ái, và nhận về một câu thủ tục. | Nước Pháp vẫn nói về ba chữ Tự do, Bình đẳng, Bác ái. Người gõ cửa, và nhận về một lời từ chối theo đúng thủ tục: đơn như thế phải đi qua Toàn quyền Đông Dương. **(viết lại)** | A label ("một câu thủ tục", "một tờ giấy hành chính", "lý do ấy") stands where the listener needs the content; it reads as a clever English summary line. Say what it said, right there. | human | reviewer, history narration sample, Oct 2026: "câu thủ tục là gì? đang hơi cụt ngủn" |

## B. Hư từ dịch từng chữ

| id | tên | English source | bad | natural | why it sounds foreign | detect | source |
|---|---|---|---|---|---|---|---|
| B01 | "một" = *a* trong câu định danh | *X is a valley / a doctor* | Hoa Lư là một thung lũng phẳng giữa núi đá vôi dựng đứng, | Hoa Lư là thung lũng phẳng lọt giữa núi đá vôi dựng đứng, | "một" is a numeral, not an article; "là một" copies *is a*. Keep it when it counts or introduces. | heur. + regex·n | r4 c04p02, c04p04, c09p01; E1 "Anh ấy là bác sĩ" |
| B02 | "một" trước nơi chốn, thể chế, sự kiện | *a court, an old citadel, a civil war, a reason* | nên quân Nguyên vào chỉ thấy một tòa thành không có lương. | nên quân Nguyên vào tới nơi chỉ thấy thành không, kho chẳng có lương. | Article reflex in front of every count noun. | regex | r4 #2 (20 rows): c04p03, c05p04, c07p01, c05p01, s0158 |
| B03 | "một cách + tính từ" | *-ly adverb, in a … manner* | Caffeine được hấp thụ một cách nhanh chóng. | Caffeine ngấm vào máu nhanh. | Vietnamese adjectives modify verbs directly. | regex | ChuotVan |
| B04 | "một" = *one* chung chung | *One must…* | Một phải cẩn thận khi đọc nguồn này. **(minh họa)** | Ta phải cẩn thận khi đọc nguồn này. **(minh họa)** | *one* is a pronoun; Vietnamese uses "ta", "người ta". | regex | linguistics report P07; E9 |
| B05 | "nó" cho vật, nơi, ý | *it* | dù tới giờ nó vẫn còn đứng đó. | dù tới giờ tường vẫn còn đứng đó. | Vietnamese repeats the noun, uses "ấy", or drops the subject; "nó" for a city or wall sounds like a child or a pet. | regex | r4 #3: c01p01, c01p03, c09p01, c04p04 |
| B06 | "nó" giả (*dummy it*) | *It is recognized that…* | Nó được công nhận rằng tỉ lệ thất nghiệp đã tăng. | Người ta thừa nhận tỉ lệ thất nghiệp đã tăng. | Expletive *it* has no Vietnamese counterpart. | regex | E6 |
| B07 | "chúng" cho đồ vật | *they* (walls, files) | Những bức tường bao quanh kinh đô. Chúng bảo vệ nó khỏi quân địch. **(minh họa)** | Những bức tường bao quanh kinh đô và giữ quân địch ở ngoài. **(minh họa)** | Same as B05, plural. | heur. | linguistics report P06; E9 |
| B08 | "các/những" = *-s* | plural *-s, the… people* | Năm kinh đô này nhìn chung chia làm hai kiểu, mà kiểu thứ nhất là những pháo đài… | Năm kinh đô này đại khái chia làm hai kiểu, kiểu thứ nhất là pháo đài… | Plural marked by habit; "các người dân" is ungrammatical. Keep emphatic "những" ("có những tảng đá nặng tới…"). | regex + regex·n | r4 c02p01; E7 |
| B09 | Chuỗi "của" | *the history of the development of…* | Lịch sử của sự phát triển của kinh tế của Việt Nam **(minh họa)** | Lịch sử kinh tế Việt Nam **(minh họa)** | Vietnamese compounds nouns or turns one into a verb. | regex + regex·n | linguistics report P19; writing-vi.md |
| B10 | "của" trước triều đại, dòng họ, địa danh | *the capital of the Hồ dynasty; Đông Anh of Hà Nội* | chọn Huế làm kinh đô của nhà Nguyễn. | chọn Huế làm kinh đô nhà Nguyễn. | Vietnamese juxtaposes; "ở" for places; an appositive for a ruler ("Triệu Đà, vua nước Nam Việt"). | heur. | r4 #7: c01p01, c08p04, c03p01, c03p04, c06p04 |
| B11 | "với" = *with* | *began with a wall; Cổ Loa with three rings* | Kinh thành Huế khởi công năm 1805 với vòng tường dài khoảng mười cây số, | Năm 1805 Kinh thành Huế khởi công, tường dài khoảng mười cây số… | *with* for parts or equipment; Vietnamese says "có" or opens a clause. "gắn với" is native. | heur. | r4 #5: c08p05, c09p02 |
| B12 | "bởi" chỉ tác nhân | *was V-ed by* | Hệ thống được triển khai bởi đội kỹ thuật. | Đội kỹ thuật triển khai hệ thống. | *by*-phrase; press Vietnamese uses it under English influence (E8). | regex | ChuotVan; E6; E8 |
| B13 | Đánh dấu thì chồng nhau | *had been…, were …ing* | Chỉ tháng trước, những cây đã xanh, mà nay chúng đang vàng. | Mới tháng trước cây cối còn xanh, mà nay đã vàng rực. | Vietnamese marks time once, by context or "còn/đã". | heur. | E1 (Cao Xuân Hạo) |
| B14 | "để" sau tính từ, *to*-infinitive | *it is not hard to; try to* | Không khó để chứng minh rằng… | Có thể dễ dàng chứng minh rằng… | "để" marks purpose; "khó V", "cố V" need no linker. | heur. | E6 |
| B15 | Loại từ sai hoặc lạm dụng "cái" | *a book, two boats* | hai cái thuyền, một cái người lính, ba cái tường **(minh họa)** | hai chiếc thuyền, một người lính, ba bức tường **(minh họa)** | Classifiers follow the noun's kind, not *a/the*. Never delete a correct classifier. | human | E5; E7 |
| B16 | "sẽ" cho *would* | future-in-the-past | Ông nói rằng ông sẽ trở về, nhưng ông đã chết trước đó. **(minh họa)** | Ông nói mình sẽ trở về, nhưng chưa kịp thì đã chết. **(minh họa)** | Backshift copied; Vietnamese tells the time relation instead. | human | linguistics report P12 |

## C. Bị động và người làm bị giấu

| id | tên | English source | bad | natural | why it sounds foreign | detect | source |
|---|---|---|---|---|---|---|---|
| C01 | "được + V" giấu người làm | *was built / was chosen / was recorded* | Câu ông nói được Toàn thư ghi lại thế này: | Toàn thư chép lại câu ông nói thế này: | "được" implies benefit; in a story the listener needs who acted. Native: "được gọi là", "được mẹ khen". | regex + regex·n | r4 #4: c07p01, s0073, c07p03; S1 "được công bố" |
| C02 | Bị động vô nhân xưng đầu câu | *It is recognized / advised that…* | Được khuyến cáo nên đến bác sĩ. | Bạn nên đến bác sĩ khám. | No dummy subject in Vietnamese; use "người ta", "nên", or the addressee. | regex | E6 |
| C03 | "bị" cho việc chưa xảy ra, không rõ ai làm | *afraid of being attacked; harder to be attacked* | Tôi đoán ông còn sợ bị đánh từ cả hai đầu đất nước, | Tôi đoán ông còn sợ giặc đánh tới từ cả hai đầu đất nước, | Names the attacker; "dễ giữ" instead of "khó bị đánh". Native adverse "bị" stays ("Thăng Long bị giặc ngoài chiếm"). | heur. | r4 c07p02 |
| C04 | Báo cáo việc mình làm bằng bị động | *will be checked / has been updated* | Ngày tháng và chi tiết dưới đây sẽ được kiểm lại ở bước research. | Ngày tháng và chi tiết mình sẽ kiểm lại ở bước research. **(viết lại)** | The agent hides itself; Vietnamese reports say who does it. | regex (chat) | S1 (bad); rewrite for this skill |
| C05 | Bị động chồng | *an approved stage is reopened* | Khi lưu một thay đổi thật, stage research đã duyệt sẽ được mở lại. | …và mở lại stage research nếu stage ấy đã approve. | Two passives in one clause, nobody acts; "đã duyệt thì mở lại", or name who reopens it. | regex | EV T3 (out-b → out-a); the judge proposed "đã được duyệt sẽ được mở lại" |

## D. Danh hóa và động từ đệm

| id | tên | English source | bad | natural | why it sounds foreign | detect | source |
|---|---|---|---|---|---|---|---|
| D01 | "việc/sự + V" | *the V-ing of; for the purpose of* | tiện cho việc làm ăn. | tiện đường làm ăn. | Nominalised action without a doer. "việc nhà", "sự thật", "cuộc khởi nghĩa" are plain nouns. | regex | r4 c02p01; vn-humanize "Việc quản lý trở nên dễ dàng hơn" |
| D02 | Động từ đệm | *conduct, carry out, make a decision* | Nhà vua đã đưa ra một quyết định để tiến hành một cuộc tấn công. | Nhà vua quyết định đem quân đánh. | Light verb + noun where Vietnamese has one verb. | regex | linguistics report P22, P20 |
| D03 | Hán cổ dịch theo chữ | literal classical phrase | dẫn họ bằng lễ nghĩa | mở trường dạy họ lễ nghĩa | Keeps the source's shape so nobody knows who did what. Also "chỉ đủ tự giữ" → "chỉ còn biết lo giữ mình". | human | WP §1 (reviewer verdicts, Hai Bà Trưng v7/v8) |
| D04 | Danh hóa câu hỏi | *the reason why, the way that* | Lý do tại sao họ thất bại là… **(minh họa)** | Họ thất bại vì… **(minh họa)** | Ask or state the cause directly. | regex | linguistics report P43 |
| D05 | "Đó là + V" làm vị ngữ | *That is choosing the lesser evil* | Đó là chọn mối nguy nhỏ hơn cho lúc ấy. | Cho Pháp vào thì Tưởng phải rút, tức là đuổi được kẻ đáng ngại hơn. | Gerund predicate; Vietnamese tells what was done and why. | heur. | S1 (both sides are agent text; the reviewer still judged the rewrite translated) |
| D06 | "những lợi ích của việc + V" | *the benefits of instruction / of V-ing* | và đem lại cho họ những lợi ích của việc học. | rồi đem sự học ấy về cho họ. | Abstract noun chain where Vietnamese uses the verb. | regex | EV T1 (out-b → out-a) |

## E. Khung, thành ngữ, logic kiểu Anh

| id | tên | English source | bad | natural | why it sounds foreign | detect | source |
|---|---|---|---|---|---|---|---|
| E01 | Thành ngữ, khung dịch chữ | *put on one map; different fates; the enemy came from; play a role; open a new chapter; the only… ever; never became* | Đặt năm kinh đô lên cùng một tấm bản đồ…, ta thấy hai kiểu kinh đô có số phận khác hẳn nhau. | Chấm cả năm kinh đô lên bản đồ… thì thấy hai kiểu kinh đô đi hai ngả khác hẳn nhau. | Each word is Vietnamese, the image is English. | regex (phrase list, open-ended) | r4 #6 (18 rows): c09p02, c08p06, c04p01, c06p06, c08p03; ChuotVan; DivEMT; E1 |
| E02 | Câu gây khiến kiểu Anh | *X made me fix…; the second decree led to a new capital* | Phản biện khiến mình sửa những chỗ này so với bản đầu: | Grok và GPT đọc chéo xong, mình sửa mấy chỗ này so với bản đầu: **(viết lại)** | Abstract causer as subject; Vietnamese tells the event, then what followed ("…mới sinh chuyện…", "nên…"). Native: "khiến ai cũng sợ". | regex | S1 (bad); r4 c08p03 "dẫn tới một kinh đô mới" → "mới sinh chuyện dựng kinh đô mới" |
| E03 | "là + tính từ" | *X is important* | Điều này là quan trọng đối với cuộc chiến. | Điều này quan trọng với cuộc chiến. | Adjectives are predicates; "là" is for identity ("Hà Nội là kinh đô"). | heur. | E5 |
| E04 | So sánh kiểu Anh | *much longer than; harder to attack; four times farther than X* | hơn bảy trăm năm, lâu hơn Tây Đô rất nhiều. | hơn bảy trăm năm, Tây Đô làm sao bì được. | English comparative frame; compare like with like ("gấp hơn bốn lần đường từ ải về Thăng Long"). Native: "sớm hơn lời hẹn hai ngày". | regex | r4 #8: c01p02, c07p02, c08p04 |
| E05 | "không chỉ… mà còn" | *not only… but also* | Không chỉ giúp tỉnh táo, cà phê mà còn mang lại nhiều lợi ích cho sức khỏe. | Một ly cà phê buổi sáng giúp tỉnh người nhanh. | Used for rhythm, not a real contrast. | heur. | ChuotVan |
| E06 | Sai vai nghĩa | same SVO, different role | Tôi ăn bàn. | Tôi ăn ở bàn. | Word-for-word drops the preposition that marks place or tool. | human | E5 (Phan Ngọc) |
| E07 | Câu nghe ra sai nghĩa đen | *the fields rose and fell with the tide* | Ruộng ấy lên xuống theo thủy triều | Ruộng ấy cấy theo con nước thủy triều lên xuống | Heard literally, the field moves. | human | WP §1 |
| E08 | Câu hỏi giao tiếp dịch chữ | *What is your name?* | Tên của bạn là gì? | Bạn tên gì? | Translate the speech act, not the words. | regex | E6 |
| E09 | "biến X thành Y" | *turned X into* | vậy mà Gia Long biến chính chỗ ấy thành nơi cả nước kéo về chầu. | vậy mà Gia Long lại lấy chính chỗ ấy làm nơi cả nước kéo về chầu. | "lấy … làm" is the Vietnamese frame for choosing a role. | heur. | r4 c08p05 |
| E10 | Từ chọn theo bản dịch, không theo lời nói | *most likely due to; Taylor's reading; gap* | cách đọc của Taylor | nhận xét của Taylor | Dictionary equivalent instead of the word a speaker uses ("chỗ hở" → "chỗ yếu", "hưởng ứng" → "cũng nổi lên theo"). | human | WP §1 |
| E11 | "trong quan hệ với" | *in relation to* | Anh ấy rất khéo trong quan hệ với khách hàng. **(minh họa)** | Anh ấy khéo chiều khách. | Names a relation without saying what it is; say what the person does for whom, or restructure. Both eval writers leaked it from the same English note ("useful to France in relation to his compatriots"); there the source is a 1911 French letter, so quote and gloss it rather than paraphrase, or the meaning shifts. | regex | EV T1 (both out-a and out-b) |
| E12 | "với tư cách (là)" | *as a(n) …* | xin vào học trường Thuộc địa với tư cách thực tập sinh. | xin vào trường Thuộc địa học làm thực tập sinh. **(viết lại)** | *as* + role; speech says "làm …", "vào làm …". Native in formal register. | regex (info) | EV T1 (out-b) |
| E13 | "sử dụng" thay "dùng" | *use* | Nút Edit trên màn hình Research sử dụng endpoint này. | Nút Edit trên màn hình Research dùng chính endpoint này. | Written-register verb in speech and chat; scanner skips it in `doc`. | regex (info, chat/narration) | EV T3: judge's proposed rewrite → out-b's own wording |

## F. Liên từ, rào đón, lời dẫn

| id | tên | English source | bad | natural | why it sounds foreign | detect | source |
|---|---|---|---|---|---|---|---|
| F01 | Liên từ nghị luận trong lời nói | *However, Therefore, In addition, Moreover* | Bên cạnh đó… Ngoài ra… Hơn nữa… | Nhưng… / Cùng lúc ấy… / bỏ nếu không có quan hệ | Essay connectives; speech uses "nhưng, nên, thế là, mà, thì, rồi". Normal in `doc` register. | regex + regex·n | tools report P12; WP |
| F02 | Rào đón chồng | *it may perhaps possibly* | Có lẽ có thể phần nào là do… | Có lẽ phần lớn là vì… | One hedge, at the strength the source allows. | regex | WP; tools report |
| F03 | Rào đón dịch | *most likely due to* | nhiều khả năng là do | tôi nghĩ phần lớn là vì | A probability phrase where a speaker says what he thinks. | regex | WP §1 |
| F04 | Thiếu hạt tình thái, nhịp nói | flat declaratives | Thế là trận đánh kết thúc. **(minh họa)** | Thế là trận đánh kết thúc rồi. **(minh họa)** | "rồi, mà, đấy, ấy, thì" mark turns and results. Use sparingly; never sprinkle. | human | E5 |
| F05 | Lời dẫn chatbot, video-essay | *Let's explore; In this article; As you can see; Feel free to* | Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách Redis lưu dữ liệu… | Redis lưu dữ liệu thường dùng trong bộ nhớ, nhờ đó hệ thống ít phải truy cập nguồn dữ liệu chậm hơn. | Talks about the text instead of the content. | regex | longhang2004/vietnamese-humanizer; ChuotVan; listening-r2 c02p01 "mời các bạn kể thêm" |
| F06 | Xưng hô kiểu *I/you* | fixed *I/you* | Tôi nói với bạn rằng bạn nên đi. (chị nói với em) **(minh họa)** | Chị bảo em nên đi. **(minh họa)** | Vietnamese pronouns carry age and relation. | human | E9 |
| F07 | Lời bình về phương pháp của người kể | *I won't choose which source…* | nên tôi không chọn cách nào | (bỏ; nói mỗi nguồn kể ra sao) | Meta about the narrator's method; the reviewer called these lines "vô nghĩa". | human | WP §1 |
| F08 | "đồng thời" làm liên từ | *and at the same time* | Endpoint này lưu nội dung vào `research/notes.md`, đồng thời giữ bản cũ trong `.history/research/`. | Endpoint lưu nội dung vào `research/notes.md`, giữ bản cũ trong `.history/research/`, và mở lại stage research nếu stage ấy đã approve. | Written connective for plain sequence; "và", a list, or two sentences. | regex (info, chat/doc) | EV T3 (out-b → out-a) |

## G. Trả lời chat

| id | tên | English source | bad | natural | why it sounds foreign | detect | source |
|---|---|---|---|---|---|---|---|
| G01 | Danh sách nhãn in đậm, dòng "Nhãn:" | slide/report template | Hỏi: một người bị Pháp truy nã, không đặt chân về được, làm sao dựng được tổ chức trong nước? | Mật thám Pháp săn lùng gắt nên ông không về nước được. Ông mở lớp ở Quảng Châu, đưa thanh niên trong nước sang học rồi cho về gây dựng cơ sở. | A form to fill, not a message to a person. | regex (chat) | S1 (both sides agent text; the reviewer still judged the rewrite translated) |
| G02 | Tiêu đề rồi câu lặp lại tiêu đề | headline + restating topic sentence | **Kết quả:** Mọi bài kiểm tra đều qua. Tất cả bài kiểm tra đã chạy thành công. **(minh họa)** | Chạy lại xong, bài kiểm tra nào cũng qua. **(minh họa)** | Says it twice; the second sentence adds nothing. | human | reviewer complaints, S1 |
| G03 | Dòng trạng thái kiểu Anh | *passed two rounds of cross-review; Measured results:; Review made me…* | Dàn ý tập 1 đã xong và đã qua hai lượt phản biện chéo (Grok và GPT), bạn duyệt giúp trước khi mình cho viết lời. | Dàn ý tập 1 xong rồi, Grok với GPT đã đọc chéo hai lượt. Bạn xem giúp, ổn thì mình cho viết lời. **(viết lại)** | Process nouns as subject ("phản biện", "kết quả"); Vietnamese says who did what. | regex (chat) | S1 (bad); rewrite for this skill |
| G04 | "Dưới đây là", "Hãy cùng" mở đầu | *Here is…; Let's…* | Dưới đây là kế hoạch chi tiết: **(minh họa)** | Mình định làm ba việc. **(minh họa)** | Chatbot opener (scanner id F05). | regex | tools report; reviewer rule |
| G05 | Câu hỏi duyệt dạng mệnh lệnh cụt | *Approve? Keep or drop?* | Giữ, hay né? | Bạn thấy sao? | Bare either/or reads curt and translated; ask as a person asks. | human | S1 (agent's own rewrite) |

## Sources

- r4 = translationese pass on a history narration script about Vietnam's capitals (74 edits; `#` numbers are its checklist; `cNNpNN/sNNNN` = chapter, paragraph, shot). L2 = its second listening review, ON = its old-new rewrite table. Internal review files, Oct 2026, not in this repo.
- WP = native reviewer verdicts on a Hai Bà Trưng narration script (v7/v8).
- S1 = one agent chat session (2026-10-24): agent replies about a history video series; the reviewer replied "viết văn tự nhiên hơn. lại giống dịch English one by word rồi", and after the later status reply, "văn giờ vẫn mang phong cách dịch từ English sang Vietnamese".
- EV = A/B eval 2026-10-26 run from S1: sources were English notes (T1) and an English README section (T3); `out-a` = Sonnet with this skill, `out-b` = Sonnet baseline, judged by a GPT-family model. Pairs are eval output, not reviewer-approved text.
- E1 Cao Xuân Hạo via VUSTA: https://vusta.vn/pgs-cao-xuan-hao-mot-trai-tim-dap-mai-cung-tieng-viet-p89024.html
- E5 Nguyễn Văn Hiệp, history of approaches to Vietnamese syntax: https://ir.library.osaka-u.ac.jp/repo/ouka/all/10920/riwl_001_019.pdf
- E6 Nguyễn Thị Thu Trang (2024), French impersonal passives into Vietnamese: https://jst-ud.vn/jst-ud/article/download/9130/6198/22061
- E7 classifiers and definiteness: https://dornsife.usc.edu/ling/wp-content/uploads/sites/50/2023/08/Bare_CL_and_Definiteness.pdf
- E8 Bruening & Tran, Vietnamese passives: https://udel.edu/~bruening/Downloads/VietnamesePassives7.pdf
- E9 Pronouns in Vietnamese: https://en.wikipedia.org/wiki/Pronouns_in_Vietnamese
- DivEMT post-edit corpus: https://arxiv.org/html/2205.12215
- ChuotVan: https://github.com/mahiepit/ChuotVan · vn-humanize: https://github.com/andyluu98/vn-humanize · vietnamese-humanizer: https://github.com/longhang2004/vietnamese-humanizer
- Research reports these rows were merged from: `viet-skill-research-internal.md`, `viet-skill-research-linguistics.md`, `viet-skill-research-tools.md` (internal working notes, 2026-10-26, not in this repo).
