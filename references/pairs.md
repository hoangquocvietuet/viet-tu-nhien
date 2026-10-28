# Real before → after pairs

Every pair below was edited by a reviewer, a native reader, or a published source; nothing is invented. Pairs are grouped by pattern id (`patterns.md`). "Bad" and "natural" are exact strings. Use them as few-shot examples and as regression cases for `scripts/viet_scan.py --selftest` (which embeds most of them).

Source keys (Oct 2026, internal review files, not in this repo): **r4** = translationese pass on a history narration script about Vietnam's capitals (74 edits after two listening rounds had passed the text; `cNNpNN/sNNNN` = chapter, paragraph, shot), **L1** / **L2** = the two listening reviews of that script, **ON** = its old-new rewrite table, **WP** = native reviewer verdicts on a Hai Bà Trưng narration script, **S1** = one agent chat session (2026-10-24, replies a native reviewer rejected as translated). `#n` = pair number in the internal research report.

## Contents

- [A. Khung câu và chủ thể](#a)
- [B. Hư từ](#b)
- [C. Bị động](#c)
- [D. Danh hóa](#d)
- [E. Khung, thành ngữ, so sánh](#e)
- [F. Liên từ, lời dẫn](#f)
- [G. Trả lời chat](#g)
- [Eval 2026-10-26: writing from English sources](#eval)
- [Giữ nguyên: sentences reviewers kept as natural](#giữ-nguyên)
- [Sửa quá tay: rewrites that made things worse](#sửa-quá-tay)
- [Mạch kể: native telling from two Vietnamese books](#mạch-kể)

<a id="a"></a>
## A. Khung câu và chủ thể

**A01 chủ thể trừu tượng**
- `Vậy không phải bức tường thì rốt cuộc cái gì giữ được một kinh đô?` → `Vậy không phải nhờ bức tường thì rốt cuộc kinh đô đứng được lâu là nhờ đâu?` [r4 c01p03/s0010, #2]
- `Vậy rốt cuộc thứ gì giữ cho một kinh đô đứng được, nếu đó không phải là bức tường?` → `Vậy không phải bức tường thì rốt cuộc cái gì giữ được một kinh đô?` [L2 c01p03, #50]. The "after" was itself rewritten in r4 (pair above): fixing word order alone left the abstract subject.
- Title `Cái gì giữ một kinh đô` → `Không phải nhờ bức tường` [r4 titles c09, #62]. The reviewer rejected the first as a calque of "What keeps a capital".
- Title `Hơn chục kinh đô, hai kiểu` → `Hơn chục nơi từng làm kinh đô` [r4 titles c02, #61]
- `Những gì sử sách còn ghi về Hai Bà nằm trong dăm cuốn sách` → `Chuyện Hai Bà nay chỉ còn chép trong dăm cuốn sách` [WP §1]

**A02 danh từ mang mệnh đề làm chủ ngữ**
- `Kinh đô ông chọn là Hoa Lư,` → `Ông chọn đất Hoa Lư làm kinh đô,` [r4 c04p01/s0043, #4]
- `Kinh đô này không mất vì thua trận mà do triều đình tự bỏ đi, còn Hoa Lư thì về sau vẫn là…` → `Hoa Lư không mất vì thua trận, mà là triều đình tự bỏ đi, và về sau nơi này vẫn là…` [L2 c04p04, #57]

**A03 câu chẻ "Thứ/Cái … là"**
- `Thứ có thật là kho tên Cầu Vực, nơi tìm thấy khoảng mười nghìn mũi tên đồng.` → `Ngoài đời thật thì có kho tên Cầu Vực, nơi đào được khoảng mười nghìn mũi tên đồng.` [r4 c03p03/s0032, #6]
- `rút khỏi thành, tôi thấy lời ấy khá khớp, cái họ giữ là dân với lương còn cái thành thì họ bỏ lại.` → `rút khỏi thành mới thấy lời ấy đúng thật, vì họ giữ lấy dân với lương còn thành thì bỏ lại.` [r4 c06p03/s0087, #7]

**A04 / A05 / A06 (external)**
- `Loại táo này là thứ mà tôi rất thích ăn.` → `Loại táo này tôi rất thích ăn.` [Nguyễn Văn Hiệp, https://ir.library.osaka-u.ac.jp/repo/ouka/all/10920/riwl_001_019.pdf]
- `Không có mặt trời ở đây.` → `Ở đây không có nắng.` [Cao Xuân Hạo, https://vusta.vn/pgs-cao-xuan-hao-mot-trai-tim-dap-mai-cung-tieng-viet-p89024.html]
- `Có nhiều xe máy ở Việt Nam.` → `Ở Việt Nam có nhiều xe máy.` [Nguyễn Văn Hiệp, same URL]
- `Người mà tôi gặp hôm qua là nhà văn.` → `Người tôi gặp hôm qua là nhà văn.` [same URL]

**A07 lời giải thích chen ngang**
- `Lúc ấy thái thú, tức viên quan nhà Hán cai cả một quận, cùng các quan Hán khác chỉ còn…` → `Trong khi đó các quan Hán ở đây, kể cả những thái thú cai cả một quận, chỉ còn…` [WP §1]
- `thế cô, đều thua chết, tức là lẻ loi yếu thế và cả hai đều thua mà chết` → `thế cô nên cả hai đều thua mà chết` [WP §1]
- `ô hợp`, `thủ cấp` glossed → just say `đầu người` [WP §1]

**A08 câu tóm-rồi-kể, câu nhãn, câu kết meta**
- `Theo tôi thì trước khi đánh nhau, mỗi bên đã dựa vào một thứ. Nhà Hán dựa vào… Còn Hai Bà dựa vào…` → `Tính ra thì đến lúc hai bên giáp mặt, nhà Hán đã có gần hai năm lo đường sá, thuyền bè và lương thực…` [WP §1]
- `và đó là chặng thứ nhất trong ba chặng` → `và chặng thứ nhất bắt đầu từ đó` [WP §1]
- `Cả khu cố đô rộng ba trăm héc ta, chỉ bằng nửa Cổ Loa, và núi đá gánh gần hết việc của tường thành.` → `Cả khu cố đô chỉ rộng ba trăm héc ta, bằng nửa Cổ Loa, vì ở đây núi đá gần như làm thay tường thành.` [ON c04p02, #55]
- `Theo các bạn, vùng nào trên đất nước mình có địa thế của một kinh đô?` → `Vậy theo các bạn, nhà Hồ mất vì chọn sai chỗ đóng đô, hay vì lòng dân không theo?` [ON c09p03, #64]

**A09 mệnh đề thời gian, mục đích đặt kiểu Anh**
- `Một người nói sau khi thắng,` → `Một người nói lúc đã thắng,` [r4 c09p03/s0162, #48]
- `kể từ khi cảnh người Việt đánh nhau trong nhà vừa dứt.` → `tính từ lúc người Việt thôi đánh nhau trong nhà.` [r4 c04p04/s0054]
- `mà rút đi trước khi giặc tới,` → `mà rút đi từ lúc giặc chưa tới,` [r4 c06p01/s0078]
- `Rồi khi quân tới Tam Điệp, ông gọi` → `Tới Tam Điệp, ông gọi` [r4 c06p05/s0097]
- `và ở đó sáu năm tới khi mất năm 944.` → `và ở đó sáu năm tới lúc mất năm 944.` [r4 c03p04/s0038]
- `khi năm 1371 vua Chế Bồng Nga` → `ấy là năm 1371, vua Chế Bồng Nga` [r4 c06p04/s0089]
- `Ông từng làm quan nhà Tiền Lê, và khi vị vua Tiền Lê cuối cùng mất thì ông lên ngôi, lập nên nhà Lý.` → `Ông vốn làm quan nhà Tiền Lê, đến lúc vua cuối cùng nhà Tiền Lê mất thì lên ngôi, lập ra nhà Lý.` [r4 c05p01/s0058]
- `Hưng Đạo dặn vua đừng vắt kiệt sức dân vào năm 1300, mười hai năm sau khi nhà Trần` → `Năm 1300 Hưng Đạo dặn vua đừng vắt kiệt sức dân, lúc ấy là mười hai năm sau lần nhà Trần` [r4 c09p03/s0160]
- `Để biết một kinh đô gần hay xa phương bắc, ta đo` → `Muốn biết kinh đô nào gần hay xa phương bắc thì ta đo` [r4 c02p02/s0020, #12]
- `Rồi mỗi lần quân phương bắc kéo xuống bằng đường bộ, Thăng Long thường hứng đòn sớm.` → `Rồi mỗi lần quân phương bắc theo đường bộ kéo xuống thì Thăng Long lại hứng đòn trước.` [r4 c05p05/s0075, #47]
- `Phía trước có núi che, biên giới thì ở xa, nên với một triều đình vừa qua nội chiến thì đây là chỗ yên ổn.` → `Trước mặt có núi che, biên giới lại ở xa, nên đây là chỗ yên ổn cho một triều đình vừa qua nội chiến.` [ON c04p03, #56]; r4 later rewrote the after-clause again (B02 below).

**A10 đuôi câu "và đó là", ", nơi sau này"**
- `và đó là lần đầu tiên Thăng Long` → `thế là lần đầu tiên Thăng Long` [r4 c06p01/s0079]
- `Đó là cửa sông Hương thông ra biển, nơi sau này hạm đội Pháp kéo vào.` → `Đó là cửa sông Hương thông ra biển, về sau hạm đội Pháp kéo vào chính từ đây.` [r4 c08p05/s0143]
- `Còn chính vùng đồng bằng quanh đó về sau lại có kinh đô trụ lâu nhất trong năm nơi, ở Thăng Long cách đó chín cây số.` → `Còn ngay trên vùng đồng bằng ấy, cách Cổ Loa chín cây số, về sau lại có Thăng Long làm kinh đô lâu nhất trong năm nơi.` [r4 c03p04/s0039, #22]

**A12 tách câu ở chỗ đổi đề**
- `vốn nắm quyền nhà Trần từ trước rồi mới lên ngôi lập ra nhà Hồ năm 1400.` → `Ông nắm quyền nhà Trần từ trước, tới năm 1400 mới lên ngôi, lập ra nhà Hồ.` [L1 c01p01, #53]
- `Các nhà khảo cổ thì dè dặt hơn, họ xác định vòng lũy giữa đắp…` → `Các nhà khảo cổ thì dè dặt hơn. Họ xác định vòng lũy ở giữa, trong ba vòng lũy của thành, được đắp…` [L2 c03p01, #54]
- `Rồi triều đình bỏ Thăng Long rút đi trước khi quân Mông Cổ kéo tới, thế là năm ấy lần đầu tiên…` → `Rồi triều đình bỏ Thăng Long mà rút đi trước khi giặc tới. Đó là lần đầu tiên…` [L2 c06p01, #58]
- `Năm 1285 người Mông Cổ đã lập ra nhà Nguyên và quân Nguyên lại kéo sang, triều đình lại bỏ thành…` → `Tới năm 1285, người Mông Cổ đã lập ra nhà Nguyên, và quân Nguyên kéo sang lần nữa. Triều đình lại bỏ thành…` [L2 c06p02, #59]
- `Quân Hán tới với đường, thuyền và lương đã lo suốt gần hai năm, còn các Lạc tướng thì có lẽ…` → `Quân Hán kéo tới với đường sá, thuyền bè và lương thực đã lo gần hai năm. Chuyện thứ hai là các Lạc tướng có lẽ…` [Hai Bà Trưng rounds, via linguistics report P44]
- `Năm 1788 Phú Xuân trở thành kinh đô của nhà Tây Sơn, nơi vua Quang Trung đóng triều.` → `Năm 1788 Phú Xuân thành kinh đô nhà Tây Sơn, và sau chiến tranh vua Quang Trung ra Chiếu khuyến nông…` [ON c08p03, #60]
- `Trường từ chối, vì đơn như thế phải đi qua Toàn quyền Đông Dương. Người gõ cửa nước Pháp của ba chữ Tự do, Bình đẳng, Bác ái, và nhận về một câu thủ tục.` → `Nước Pháp vẫn nói về ba chữ Tự do, Bình đẳng, Bác ái. Người gõ cửa, và nhận về một lời từ chối theo đúng thủ tục: đơn như thế phải đi qua Toàn quyền Đông Dương.` [A14 + E: "nước Pháp của ba chữ" is *the France of liberty…*; the label "một câu thủ tục" needs its content; reviewer, history narration sample, Oct 2026; right side is a rewrite. Do not write "Người tin ba chữ… nên gõ cửa": no source gives that motive in 1911]

<a id="b"></a>
## B. Hư từ

**B01 "là một", "một" thừa**
- `Hoa Lư là một thung lũng phẳng giữa núi đá vôi dựng đứng,` → `Hoa Lư là thung lũng phẳng lọt giữa núi đá vôi dựng đứng,` [r4 c04p02/s0045, #13]
- `Hoa Lư không mất vì thua trận, mà là triều đình tự bỏ đi, và về sau nơi này vẫn là một thành quân sự quan trọng.` → `Hoa Lư không mất vì thua trận mà vì triều đình tự bỏ đi, và về sau nơi này vẫn là chỗ đóng quân quan trọng.` [r4 c04p04/s0053, #15]
- `mà thành phố vẫn là một đô thị lớn.` → `mà phố xá vẫn đông nghịt người.` [r4 c09p01/s0152]
- `Nên tôi tin một kinh đô trụ được là nhờ hai thứ, đồng lúa đủ nuôi quân và người dân còn ủng hộ triều đình.` → `Nên tôi tin kinh đô trụ được là nhờ đồng lúa đủ nuôi quân, và nhờ dân còn ủng hộ triều đình.` [r4 c09p01/s0154, #10]
- `Lại có nơi qua mỗi thời mang một tên khác, như Đại La về sau đổi tên thành Thăng Long.` → `Lại có nơi mỗi thời một tên, như Đại La về sau đổi thành Thăng Long.` [r4 c02p01/s0016, #34]
- `Nhưng đúc được chừng ấy mũi tên, lại thêm trống đồng, thì chắc ở đây đã có một nhà nước đủ thợ đúc vũ khí cả loạt.` → `Nhưng đúc được chừng ấy mũi tên lại thêm trống đồng thì chắc ở đây đã có nhà nước, có đủ thợ đúc vũ khí hàng loạt.` [r4 c03p03/s0034]
- `Giặc đã tới thật, vua Trần Thái Tông hỏi ý Thái sư Trần Thủ Độ, một đại thần trong triều.` → `Giặc tới thật rồi, vua Trần Thái Tông mới hỏi ý đại thần Trần Thủ Độ, người đang giữ chức Thái sư.` [r4 c06p01/s0077]
- `Anh ấy là một bác sĩ.` → `Anh ấy là bác sĩ.` [Cao Xuân Hạo, via linguistics report P13]

**B02 "một" trước nơi chốn, thể chế, sự kiện**
- `nên đây là chỗ yên ổn cho một triều đình vừa qua nội chiến.` → `nên triều đình vừa qua nội chiến ngồi ở đây thấy yên ổn.` [r4 c04p03/s0050, #14]
- `một tờ chiếu ngắn gửi cho cả triều đình đọc.` → `rồi cho đọc trước cả triều đình, chiếu ấy ngắn thôi.` [r4 c05p01/s0057, #16]
- `Đến cuối chiếu, một ông vua vừa lên ngôi lại hỏi ý cả triều bằng một câu rất ngắn:` → `Đến cuối chiếu, ông vua mới lên ngôi ấy lại quay sang hỏi cả triều đúng một câu:` [r4 c05p01/s0059, #17]
- `nên quân Nguyên vào chỉ thấy một tòa thành không có lương.` → `nên quân Nguyên vào tới nơi chỉ thấy thành không, kho chẳng có lương.` [r4 c06p02/s0081, #18]
- `xây trên nền một tòa thành cũ.` → `xây chồng lên nền thành cũ.` [r4 c05p04/s0070, #40]
- `triều đình lại về núp sau một pháo đài.` → `triều đình lại về núp sau pháo đài.` [r4 c07p01/s0109]
- `Ông trả lời bằng một câu mà Toàn thư còn chép lại:` → `Ông trả lời một câu mà Toàn thư còn chép lại:` [r4 c06p03/s0085]
- `Lý Công Uẩn thì nói rõ một lý do vì dân khi chọn đất, một nơi rộng và cao ráo dù gần phương bắc hơn.` → `Lý Công Uẩn thì khi chọn đất đã nói rõ là vì dân, chọn chỗ rộng mà cao ráo dù gần phương bắc hơn.` [r4 suspicious phrases s0158, #27]

**B03** `Caffeine được hấp thụ một cách nhanh chóng.` → `Caffeine ngấm vào máu nhanh.` [ChuotVan, https://github.com/mahiepit/ChuotVan]

**B05 "nó"**
- `Người cho xây nó là` → `Người cho xây thành là` [r4 c01p01/s0003, #19]
- `dù tới giờ nó vẫn còn đứng đó.` → `dù tới giờ tường vẫn còn đứng đó.` [r4 c01p01/s0005, #20]
- `Theo tôi, đó là vùng đông dân và nhiều lúa ở quanh nó.` → `Theo tôi là nhờ vùng đông dân và nhiều lúa ở xung quanh.` [r4 c01p03/s0011, #3/#21]
- `còn cái triều đình núp sau nó thì` → `còn triều đình núp sau bức tường ấy thì` [r4 c09p01/s0151, #23]
- `Vậy mà cộng lại, nó vẫn làm kinh đô hơn bảy trăm năm.` → `Vậy mà cộng lại thì vẫn làm kinh đô được hơn bảy trăm năm.` [r4 c09p01/s0153, #24]
- `Người quyết định bỏ nó mà đi là vua Lý Công Uẩn, ông vua đầu tiên của nhà Lý.` → `Người quyết định bỏ vòng núi ấy mà đi là Lý Công Uẩn, vua đầu tiên nhà Lý.` [r4 c04p04/s0055]
- `Vậy mà cộng hết những quãng làm kinh đô lại, nó vẫn đứng được hơn bảy trăm năm` → `Vậy mà cộng hết những quãng làm kinh đô lại, Thăng Long vẫn làm kinh đô được hơn bảy trăm năm` [L2 c01p02, #49]

**B06** `Nó được công nhận rằng tỉ lệ thất nghiệp đã tăng.` → `Người ta thừa nhận tỉ lệ thất nghiệp đã tăng.` [Nguyễn Thị Thu Trang 2024, https://jst-ud.vn/jst-ud/article/download/9130/6198/22061]

**B08 các/những**
- `Năm kinh đô này nhìn chung chia làm hai kiểu, mà kiểu thứ nhất là những pháo đài dựa vào lũy đất, núi đá hay tường đá để giữ mình.` → `Năm kinh đô này đại khái chia làm hai kiểu, kiểu thứ nhất là pháo đài dựa vào lũy đất, núi đá hay tường đá mà giữ mình.` [r4 c02p01/s0018, #11]
- `vậy mà cộng hết các quãng lại thì` → `vậy mà cộng dồn lại thì` [r4 c01p02/s0009, #32]
- `người bản địa… hưởng ứng` → `dân… cũng nổi lên theo` [WP §1]

**B10 "của" trước tên**
- `kinh đô của nhà Hồ lúc ấy.` → `lúc ấy là kinh đô nhà Hồ.` [r4 c01p01/s0001, #31]
- `nay thuộc xã Đông Anh của Hà Nội,` → `nay là xã Đông Anh ở Hà Nội,` [r4 c03p01/s0023, #36]
- `Theo cách tính thường gặp thì khoảng năm 179 trước Công nguyên, Âu Lạc rơi vào tay Triệu Đà của nước Nam Việt.` → `Sách vở thường tính là khoảng năm 179 trước Công nguyên thì Âu Lạc rơi vào tay Triệu Đà, vua nước Nam Việt.` [r4 c03p04/s0035, #37]
- `chọn Huế làm kinh đô của nhà Nguyễn.` → `chọn Huế làm kinh đô nhà Nguyễn.` [r4 c08p04/s0136, #41]
- `lại là đất gốc của họ Nguyễn` → `lại là đất gốc họ Nguyễn` [r4 c08p04/s0138, #42]
- `tức vùng Từ Sơn của Bắc Ninh bây giờ,` → `tức vùng Từ Sơn ở Bắc Ninh bây giờ,` [r4 c06p04/s0090]

**B11 "với" = with**
- `Kinh thành Huế khởi công năm 1805 với vòng tường dài khoảng mười cây số, dọc tường có hai mươi bốn pháo đài.` → `Năm 1805 Kinh thành Huế khởi công, tường dài khoảng mười cây số và dọc tường có hai mươi bốn pháo đài.` [r4 c08p05/s0140]
- `là Cổ Loa với ba vòng lũy đất,` → `là Cổ Loa có ba vòng lũy đất,` [r4 c09p02/s0156]

**B12** `Hệ thống được triển khai bởi đội kỹ thuật.` → `Đội kỹ thuật triển khai hệ thống.` [ChuotVan]; `Email đã được nhận bởi một số nhân viên.` → `Một số nhân viên đã nhận được email.` [linguistics report P30, after E8 https://udel.edu/~bruening/Downloads/VietnamesePassives7.pdf]

**B13** `Chỉ tháng trước, những cây đã xanh, mà nay chúng đang vàng.` → `Mới tháng trước cây cối còn xanh, mà nay đã vàng rực.` [Cao Xuân Hạo, VUSTA URL above]

**B14** `Không khó để chứng minh rằng…` → `Có thể dễ dàng chứng minh rằng…` [Nguyễn Thị Thu Trang 2024]

<a id="c"></a>
## C. Bị động

- C01 `được khởi công từ năm 1397,` → `khởi công từ năm 1397,` [r4 c07p01/s0103, #25]
- C01 `còn Thăng Long thì được chọn để người các nơi kéo về` → `còn Thăng Long thì Lý Công Uẩn chọn để người các nơi kéo về` [r4 suspicious phrases s0073, #26; a cue pinned the old words, so the script kept them]
- C01 `Câu ông nói được Toàn thư ghi lại thế này:` → `Toàn thư chép lại câu ông nói thế này:` [r4 c07p03/s0118, #29]
- C01 `Kết: Bác mất ngày 2/9/1969 nhưng được công bố là 3/9. Năm 1989 mới đính chính.` → `Bác mất ngày 2/9/1969, nhưng hồi đó công bố là ngày 3, tới năm 1989 mới nói lại cho đúng.` [S1, agent's own rewrite]
- C02 `Được công nhận rằng quá trình phân bào…` → `Người ta công nhận quá trình phân bào…`; `il est conseillé de consulter…` rendered `Được khuyến cáo nên đến bác sĩ.` → `Bạn nên đến bác sĩ khám.` [Nguyễn Thị Thu Trang 2024]
- C03 `Tôi đoán ông còn sợ bị đánh từ cả hai đầu đất nước,` → `Tôi đoán ông còn sợ giặc đánh tới từ cả hai đầu đất nước,` [r4 c07p02/s0115, #28]
- C04 `Ngày tháng và chi tiết dưới đây sẽ được kiểm lại ở bước research.` [S1, bad only] → rewrite for this skill: `Ngày tháng và chi tiết mình sẽ kiểm lại ở bước research.`

<a id="d"></a>
## D. Danh hóa

- D01 `tiện cho việc làm ăn.` → `tiện đường làm ăn.` [r4 c02p01/s0019, #35]
- D01 `Việc quản lý trở nên dễ dàng hơn.` → `Báo cáo tuần giờ có trong 15 phút thay vì cả buổi chiều.` [vn-humanize, https://github.com/andyluu98/vn-humanize]
- D01 `Triều đình dời về sau thành đá rốt cuộc chỉ trụ được chừng chín năm.` → `Tính ra từ ngày dời về sau thành đá, triều đình chỉ trụ được chừng chín năm.` [r4 c07p03/s0121]
- D03 `dẫn họ bằng lễ nghĩa` → `mở trường dạy họ lễ nghĩa`; `lấy pháp luật trói buộc` → `đem luật lệ ra bó buộc`; `nhắc lại điều lệ cũ để ràng buộc` → `đem luật lệ cũ ra ban bố lại để buộc họ phải theo`; `Chỉ đủ tự giữ` → `chỉ còn biết lo giữ mình` [WP §1, reviewer verdicts]
- D05 `Trả lời: để khoảng 200.000 quân Tưởng rút về. Đó là chọn mối nguy nhỏ hơn cho lúc ấy.` → `Lý do là lúc đó gần 200.000 quân Tưởng đang đóng ở miền Bắc. Cho Pháp vào thì Tưởng phải rút, tức là đuổi được kẻ đáng ngại hơn.` [S1, agent's own rewrite]

<a id="e"></a>
## E. Khung, thành ngữ, so sánh

**E01 khung, thành ngữ dịch chữ**
- `Đặt năm kinh đô lên cùng một tấm bản đồ từ Cổ Loa ngoài Bắc tới Huế ở miền Trung, ta thấy hai kiểu kinh đô có số phận khác hẳn nhau.` → `Chấm cả năm kinh đô lên bản đồ, từ Cổ Loa ngoài Bắc tới Huế ở miền Trung, thì thấy hai kiểu kinh đô đi hai ngả khác hẳn nhau.` [r4 c09p02/s0155, #9]
- `và lần này kẻ thù đến từ biển.` → `và lần này giặc kéo vào từ phía biển.` [r4 c08p06/s0146]
- `Ông vừa trải qua cả một cuộc nội chiến, nên tôi đoán` → `Nội chiến vừa mới dứt, nên tôi đoán` [r4 c04p01/s0044, #5/#38]
- `Quân Thanh cũng chẳng phải đạo quân ngoại bang duy nhất từng vào thành,` → `Cũng đâu phải mỗi quân Thanh từng vào được thành này,` [r4 c06p06/s0101]
- `và Nghệ An không bao giờ thành kinh đô.` → `và Nghệ An rốt cuộc chẳng thành kinh đô.` [r4 c08p03/s0135]
- `Một bên tường dày mà mất nhanh, một bên bị chiếm đi chiếm lại mà vẫn trụ lâu,` → `Thành tường dày thì mất nhanh, còn thành bị chiếm đi chiếm lại thì lại trụ lâu,` [r4 c01p03/s0010, #1]
- `Cả chuỗi có chung một sợi chỉ là câu Bác dặn cụ Huỳnh Thúc Kháng năm 1946` → `Cả chuỗi xoay quanh câu Bác nói năm 1946` [S1, agent's own rewrite]
- `Cà phê đóng vai trò vô cùng quan trọng trong thói quen hằng ngày.` → `Một ly cà phê buổi sáng giúp tỉnh người nhanh.` [ChuotVan]
- `Các tuyến nước nội địa có thể là một chủ đề tốt để xây dựng một kì nghỉ.` → `Du lịch bằng đường thủy nội địa là một ý tưởng nghỉ dưỡng không tồi.` [DivEMT MT → professional post-edit, https://arxiv.org/html/2205.12215]
- `Cúi xin bệ hạ bước ra khỏi mặt trời của kẻ hạ thần.` → `Tránh ra cho ta sưởi nắng.` [Cao Xuân Hạo]

**E02 câu gây khiến**
- `Một tờ lo chuyện ruộng, một tờ lo chuyện trông coi đất nước, và chính tờ thứ hai dẫn tới một kinh đô mới.` → `Tờ thì lo ruộng, tờ thì lo trông coi đất nước, mà chính tờ thứ hai mới sinh chuyện dựng kinh đô mới.` [r4 c08p03/s0132, #8]
- `Phản biện khiến mình sửa những chỗ này so với bản đầu:` [S1, bad only; the reviewer answered "văn giờ vẫn mang phong cách dịch"] → rewrite for this skill: `Grok và GPT đọc chéo xong, mình sửa mấy chỗ này so với bản đầu:`

**E04 so sánh**
- `hơn bảy trăm năm, lâu hơn Tây Đô rất nhiều.` → `hơn bảy trăm năm, Tây Đô làm sao bì được.` [r4 c01p02/s0009, #43]
- `Tây Đô khó bị đánh hơn,` → `Tây Đô dễ giữ hơn,` [r4 c07p02/s0114, #44]
- `xa gấp hơn bốn lần Thăng Long, nên giặc phương bắc muốn đánh tới cũng phải đi xa hơn nhiều.` → `gấp hơn bốn lần đường từ ải về Thăng Long, nên giặc phương bắc muốn đánh tới thì phải đi xa hơn nhiều.` [r4 c08p04/s0139, #45]

**E09** `vậy mà Gia Long biến chính chỗ ấy thành nơi cả nước kéo về chầu.` → `vậy mà Gia Long lại lấy chính chỗ ấy làm nơi cả nước kéo về chầu.` [r4 c08p05/s0141, #46]

**E10 từ chọn theo bản dịch**
- `còn chính xác là bao nhiêu thì` → `còn đúng bao nhiêu nơi thì` [r4 c02p01/s0014, #33]
- `tràn xuống nhắm thẳng Thăng Long,` → `tràn xuống kéo thẳng về Thăng Long,` [r4 c06p01/s0076]
- `Chỗ ấy vốn là đất thấp của châu thổ sông Hồng mà người ta đã tháo nước cho khô, đủ thấy chuyện trị thủy ở đây quan trọng thế nào.` → `Chỗ ấy vốn là đất trũng ở châu thổ sông Hồng, người ta đã tháo nước cho khô, nên ở đây trị thủy là việc lớn.` [r4 c05p04/s0071]
- `Ông vừa đi lên từ cảnh nội chiến` → `Ông vừa dẹp xong một cuộc nội chiến` [L2 c04p01, #51]
- `Sử cũ chép rằng thuyền vua vừa tới Đại La thì có rồng vàng hiện ra` → `Sử cũ chép rằng thuyền vua vừa tới Đại La thì có rồng vàng bay lên` [L2 c05p04, #52]
- `nên cả ba lần giặc vào được kinh đô, thành đều về lại tay nhà Trần.` → `nên cả ba lần giặc vào được kinh đô thì rốt cuộc thành vẫn về tay nhà Trần.` [r4 c06p02/s0083]
- `cách đọc của Taylor` → `nhận xét của Taylor`; `chỗ hở` → `chỗ yếu` [WP §1]
- `Lên nhanh / tan nhanh`, `mọi thứ tan` → the reviewer's own words: `tất cả lại tan rã`, `thành công cốc`, `dã tràng` [WP §1]

<a id="f"></a>
## F. Liên từ, lời dẫn

- F03 `nhiều khả năng là do` → `tôi nghĩ phần lớn là vì`, `có lẽ` [WP §1]
- F05 `Video này chỉ chọn kể năm kinh đô, còn những nơi khác thì mời các bạn kể thêm ở phần bình luận.` → `Video này chỉ kể năm kinh đô, những nơi còn lại các bạn cứ kể thêm ở phần bình luận.` [L2 c02p01, #63]
- F05 `Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách Redis lưu dữ liệu…` → `Redis lưu dữ liệu thường dùng trong bộ nhớ, nhờ đó hệ thống ít phải truy cập nguồn dữ liệu chậm hơn.` [https://github.com/longhang2004/vietnamese-humanizer]
- F05 `Hãy cùng khám phá những lợi ích tuyệt vời này nhé!` → `Caffeine ngấm vào máu chỉ sau vài phút và rõ nhất sau khoảng một tiếng.` [ChuotVan]
- F05 `Chắc chắn rồi! Trong thời đại 4.0 ngày nay, AI không chỉ là một công cụ mà còn là người bạn đồng hành…` → `Phòng tôi bắt đầu dùng AI từ tháng trước, chủ yếu để soạn email và tóm tắt biên bản họp.` [vn-humanize]
- Quote lead-ins: `Trong đó có một chi tiết là lời…` → `Trong đó có lời…`; `Cụ thể thì sách chép rằng` → `Câu ấy chép rằng` [WP §1]

<a id="g"></a>
## G. Trả lời chat

From S1. Both sides are agent text: the first reply drew "viết văn tự nhiên hơn. lại giống dịch English one by word rồi"; the agent's rewrite is better but not approved (the reviewer later said the prose "vẫn mang phong cách dịch"). Treat the right side as a direction, not a model answer.

- G01 `Hỏi: một người bị Pháp truy nã, không đặt chân về được, làm sao dựng được tổ chức trong nước?` / `Trả lời: lớp huấn luyện ở Quảng Châu, Hội Việt Nam Cách mạng Thanh niên và sách "Đường Kách mệnh".` → `Mật thám Pháp săn lùng gắt nên ông không về nước được. Ông mở lớp ở Quảng Châu, đưa thanh niên trong nước sang học rồi cho về gây dựng cơ sở.`
- G01 `Trả lời: bàn hội nghị do các nước lớn quyết. Liên Xô và Trung Quốc muốn hoà vì việc riêng của họ, đổi lại một lời hứa tổng tuyển cử năm 1956.` → `Liên Xô và Trung Quốc đều muốn yên chuyện để lo việc nhà mình, nên ép Việt Nam nhận chia đôi ở vĩ tuyến 17, kèm lời hứa hai năm sau sẽ bầu cử thống nhất.`
- G01 `Bài học: lời hứa trên giấy không ai bảo đảm thì thành chiến tranh.` → `Điều rút ra: lời hứa không ai đứng ra bảo đảm thì sớm muộn cũng thành chiến tranh.`
- G01 `Trả lời: chọn đúng khoảng trống giữa lúc Nhật đầu hàng và lúc Đồng minh vào, cộng với thứ dân cần nhất giữa nạn đói là thóc (phá kho thóc).` → `Lực lượng nhỏ mà làm được việc lớn là nhờ chờ đúng lúc và lo đúng cái dân đang cần nhất.`
- `Mục tiêu (độc lập, thống nhất) giữ nguyên, còn cách đi thì mỗi tập một kiểu.` → `Nghĩa là độc lập và thống nhất thì giữ chắc, còn cách đi thì tùy lúc mà đổi.`
- `Bạn chốt giúp ba điểm:` / `1. Dàn ý này được chưa? Tập nào muốn đổi câu hỏi?` → `Bạn xem giúp:` / `1. Dàn ý được chưa, có tập nào muốn đổi không?`
- G05 `Mình nghĩ có những chuyện này thì phim mới sâu, và tất cả đều đã có trong sử chính thống. Giữ, hay né?` → `Mình muốn giữ vì có những chuyện này phim mới sâu, và sử chính thống đều đã nhắc tới. Bạn thấy sao?`
- `Hai câu lần trước vẫn chờ bạn: nét vẽ (người tỉ lệ khoảng 5 đầu, bỏ ký hiệu hài) và có cho xoá cache render…` → `Hai việc lần trước vẫn chờ bạn: vẽ người cao khoảng 5 đầu và bỏ mấy ký hiệu hài, và có cho xóa cache render…`
- G03 `Dàn ý tập 1 đã xong và đã qua hai lượt phản biện chéo (Grok và GPT), bạn duyệt giúp trước khi mình cho viết lời.` [bad only] → rewrite for this skill: `Dàn ý tập 1 xong rồi, Grok với GPT đã đọc chéo hai lượt. Bạn xem giúp, ổn thì mình cho viết lời.`
- G03 `Kết quả đo được: probe SUMMARY gate=1/1 screen=23/23…` [another session, bad only] → rewrite for this skill: `Mình chạy lại hết rồi: probe đủ 41/41, make test qua cả 50 package.`

<a id="eval"></a>
## Eval 2026-10-26: writing from English sources

Eval output (A/B run from S1). Sonnet wrote Vietnamese from English notes (T1) and an English README section (T3): `out-a` with this skill, `out-b` without. Both kept English structure where they wrote from the English; the skill helped a little. Neither side is reviewer-approved; the right side is the better eval wording or, where marked, a rewrite.

- E11 `có ích cho nước Pháp trong quan hệ với đồng bào` (out-a) / `có ích cho nước Pháp trong quan hệ với đồng bào mình` (out-b), from *useful to France in relation to his compatriots*: both writers leaked it. No safe paraphrase: the sentence renders a 1911 French letter, and a smooth retelling ("giúp người Pháp trông coi đồng bào") changes its meaning. Quote the locked wording with a plain gloss instead.
- D06 `và đem lại cho họ những lợi ích của việc học.` (out-b, *bring them the benefits of instruction*) → `rồi đem sự học ấy về cho họ.` (out-a)
- E12 `xin vào học trường Thuộc địa với tư cách thực tập sinh.` (out-b, *seeking admission as an intern*) → rewrite: `xin vào trường Thuộc địa học làm thực tập sinh.`
- A13 `Nếu file đã bị thay đổi kể từ lúc tải, endpoint trả về lỗi 409.` (out-b) → `Nếu file đã đổi từ lúc được tải lên màn hình, endpoint trả 409 và không ghi gì.` (out-a)
- C05 `Khi lưu một thay đổi thật, stage research đã duyệt sẽ được mở lại.` (out-b) → `…và mở lại stage research nếu stage ấy đã approve.` (out-a); also `stage research đang ở trạng thái duyệt thì mở lại`. The judge proposed the worse `stage research đã được duyệt sẽ được mở lại`.
- F08 `Endpoint này lưu nội dung vào research/notes.md, đồng thời giữ bản cũ trong .history/research/.` (out-b) → `Endpoint lưu nội dung vào research/notes.md, giữ bản cũ trong .history/research/, và mở lại stage research nếu stage ấy đã approve.` (out-a)
- E13 `Nút Edit trên màn hình Research sử dụng endpoint này.` (the judge's proposed rewrite) → `Nút Edit trên màn hình Research dùng chính endpoint này.` (out-b's own wording)
- Judge rewrites that are themselves translated (do not adopt): `Mình bổ sung 3 bài test, cả ba đều đạt` for `Mình thêm 3 test, đều qua`; `Theo cách tường thuật phổ biến` for `Theo sách sử thường kể`; `Lệnh build, tsc và vitest đều chạy thành công`.
- Addressing: out-b answered a `mình/bạn` log with `anh/em` ("Xong rồi anh nhé", "Em thêm màn hình Research"). Use the pronouns the user uses.

<a id="giữ-nguyên"></a>
## Giữ nguyên

Sentences reviewers looked at and kept as natural Vietnamese ([r4] "Suspicious phrases kept on purpose"). Use them as negative tests: the rewrite is wrong if it "fixes" these.

- `có những tảng đá nặng tới…` (emphatic "những")
- `lúc ấy họ đang sợ nhất điều gì`
- `Các nhà khảo cổ thì dè dặt hơn`
- `nên pháo đài này vẫn gắn với đường sông` ("gắn với" is native)
- `nhưng đó là truyền thuyết`
- `xa hơn Thăng Long gần bảy mươi cây số` (native comparative with a measured gap)
- `nên triều đại chẳng được lâu bền` (the decree's own wording)
- `Nơi ông chọn là thành Đại La` (natural topic-first opening)
- `truyền cho ba quân những lời bộ tiểu thuyết lịch sử Hoàng Lê nhất thống chí chép lại:` (bookish, not English-shaped)
- `sớm hơn lời hẹn hai ngày`
- `Bên ngoài còn một vòng tường đất` ("còn một" = one more)
- `Thăng Long ba lần bị giặc… đốt phá`, `Thăng Long bị giặc ngoài chiếm ít nhất sáu lần` (adverse "bị")
- `và được gọi là chúa` ("được gọi là" = called)
- `Trong một tờ chiếu khác` ("một… khác")
- `thủ đô của cả nước thống nhất` (fixed phrase)
- `Ngược lại ở Thăng Long`
- `Một người nói…, một người nói…` (native parallel)
- `có lẽ vì… nên…` (spoken causal frame)

From the linguistics sources (natural, must survive any pass): `Hai quyển sách anh cho tôi thì tôi đã đọc xong một quyển.` (topic + "thì"), `Nam bị thầy phạt`, `chị được mẹ khen`, `Hà Nội là kinh đô`, `Tôi gặp một người lính ở cổng.` (introducing "một").

<a id="sửa-quá-tay"></a>
## Sửa quá tay

Rewrites that a reviewer or the fact-check rejected because the "more natural" version changed the meaning (internal report §5).

1. `Thắng địa nghĩa là đất tốt nhất, tức là một chỗ cao ráo cho dân ở mà thuyền bè từ bốn phía đều đổ về được.` was too strong; safer: `Đọc tới đây thì ta hiểu thắng địa là đất rất thuận lợi, nói nôm na là cao ráo cho dân ở, lại là chỗ đường sá bốn phía tụ về.` The source supports "thuận lợi", not "tốt nhất".
2. `sau Cổ Loa và Hoa Lư, đây là lần đầu một triều đình chọn kinh đô vì cái ăn cái ở của dân.` → `Theo tôi, đây là lần đầu trong mấy kinh đô ta kể mà triều đình nói rõ chuyện dân sống ra sao.` An absolute "lần đầu" had to be scoped to the video.
3. `đã được tháo nước, tức là phải tháo nước đi mới cao ráo được như lời chiếu.` invented a cause; replaced by a sentence that only says the land was drained.
4. `Đặt lời ấy cạnh ba lần nhà Trần rút khỏi thành thì thấy khớp` → `Nghĩ lại ba lần nhà Trần rút khỏi thành thì đúng thế`: smoother, but the fact-check preferred the older `tôi thấy khớp`, which marks it as the narrator's reading.
5. `Vậy mà Thăng Long vẫn là kinh đô, vì vua chỉ lánh đi một quãng ngắn…` needs `Tôi nghĩ phần lớn là vì…`; dropping the hedge turns an inference into a fact.
6. `Tướng Tây Sơn giữ Thăng Long làm y như nhà Trần…` → `Tướng Tây Sơn cũng bỏ thành, giữ lực lượng rồi lui về Tam Điệp…`: "y như" claimed the same strategy and motive, which no source says.
7. Changing every `bị/được`: see Giữ nguyên.
8. `Phương án này có thể giảm thời gian chờ, nhưng chưa được thử vào giờ cao điểm.` must not become `Phương án này giảm thời gian chờ` (lost hedge and scope) [https://github.com/cuongducle/viet-humanize].

<a id="mạch-kể"></a>
## Mạch kể

Not before → after pairs: verbatim excerpts of native Vietnamese storytelling about Hồ Chí Minh's early years, for SKILL § Mạch kể. Sources opened Oct 2026: **TDT** = Trần Dân Tiên, *Những mẩu chuyện về đời hoạt động của Hồ Chủ tịch* (1948), https://talawas.org/bai/nhung-mau-chuyen-ve-doi-hoat-dong-cua-ho-chu-tich/ ; **TL** = T. Lan, *Vừa đi đường vừa kể chuyện* (1963), http://www.geocities.ws/xoathantuong/hcm_tlan.htm (the btllang.mod.gov.vn copy timed out). Full notes: `corpus/mach-ke-corpus.md` (30 excerpts). Learn the joins, not the period voice.

**Time counted from the last event, with something in it**
- `Ngày thứ hai tôi viết thư xin phép được gặp Hồ Chủ tịch. Ngay chiều hôm ấy, tôi rất sung sướng nhận được thư trả lời của Hồ Chủ tịch viết như thế này:` [TDT]
- `Sau hội nghị ít lâu, Bác đi Thuỵ Sĩ, sang Ý để dần dà đi về Tổ quốc.` [TL]
- `Đến Quảng Châu được ít lâu, Bác cùng các đồng chí Lê Hồng Phong, Hồ Tùng Mậu, Lê Tản Anh… tổ chức Việt Nam Thanh niên Cách mạng Đồng chí Hội…` [TL]

**Cause then consequence, told as events ("vì… nên", "thế là")**
- `Vì bọn đốc công Pháp rất tàn bạo, nước độc và lương thực thiếu nên nhiều người phu bị chết, những người sống thì đều đau ốm.` [TDT]
- `…‘Không sao! Tôi sẽ bàn với anh em xe lửa Đức giúp cho đồng chí…’ Thế là bước đầu đã thành công.` [TL]

**Turn against what the listener expected ("nhưng", "không ngờ")**
- `Tên quan năm Lơ–pa–dơ kéo quân từ Lạng Sơn lên hòng cứu thoát quân địch từ Cao Bằng chạy xuống. Nhưng đến nửa đường thì đoàn quân của y bị đánh tan và y bị tóm cổ.` [TL]
- `Chúng tôi đã mừng và khẽ bảo nhau: ‘Bây giờ khỏi cuốc bộ rồi!’. Không ngờ Bác bảo đồng chí cán bộ ‘đưa xe về cho bộ đội dùng chở tiếp tế…’` [TL]

**Hook from what is still missing**
- `Nhưng anh không đi. Anh muốn làm gì? Một vị trí thức ở Sài Gòn kể lại cho tôi:` [TDT]
- `Chính ông Mai ở Hải Phòng, nhân viên cũ trên một chiếc tàu Pháp của hãng ‘Vận tải hợp nhất’ đã cho chúng tôi biết những điều mà ông Lê không rõ. Ông Mai kể lại:` [TDT]

**Next sentence picks up the last one's topic**
- `Bác đến Thượng Hải đã lâu mà vẫn chưa bắt được liên lạc. Đối với người cách mạng, không gì khổ tâm bằng đã không hoạt động được…` [TL]
- `Anh ta được ít lương, nhưng anh học được nhiều chuyện mới lạ.` [TDT]

**Long sentence carries the sequence, short one lands**
- `Phụ bếp trên tàu, mỗi ngày anh ta phải làm từ bốn giờ sáng, quét dọn sạch sẽ nhà bếp lớn trên tàu, tối đốt lửa trong các lò. Sau đó đi khuân than, rồi xuống hầm lấy rau, thịt cá, nước đá v.v.` [TDT]
- `Mỗi ngày, chín giờ tối, công việc mới xong. Anh Ba mệt lử. Nhưng trong khi chúng tôi nghỉ hoặc đánh bài, anh Ba đọc hay viết đến mười một giờ hoặc nửa đêm.` [TDT]
- `Hôm ấy mới bốn giờ chiều, nhưng đã đi được ngót 40 cây số.` [TL]

**Thing, sound, body instead of a label**
- `Có nhiều cái chảo bằng đồng lớn và nặng quá, đến nỗi anh Ba phải kéo lê trên sàn. Và những cái nồi cao quá, anh phải leo lên ghế để chùi nồi.` [TDT]
- `Gọi là ‘cáng’ cho vui, chứ sự thật chỉ là một tấm vải thô, hai đầu cột chặt vào một đoạn tre, một người có thể nằm để hai người khiêng.` [TL]
- `Trong phòng có một cái bàn làm việc, một chiếc giường, một tủ sách nhỏ kê sát vào tường, và hai bàn nhỏ của hai thư ký. Phía trên lò sưởi, có một lọ hoa.` [TDT]

**Narrator states the limits of his memory** (fits a hedge in narration)
- `Chuyện này bắt đầu cách đây đã 40 năm về trước. Chúng tôi được nghe kể lại cách đây hơn 10 năm. Tôi nhớ được thế nào xin thuật lại thế ấy.` [TL]

**Question chain and call-back** (SKILL step 2b; history narration sample, 2026-10-27). Each sentence was clean but the paragraph did not link; the reviewer: "cảm giác content chưa liên kết".
- `Đầu tháng 7/1911, tàu cập cảng Marseille. Tới đất Pháp rồi, Nguyễn Tất Thành vẫn làm thuê cho hãng Năm Sao. Ở Pháp được hơn hai tháng thì Người viết một lá thư… Cũng trong thời gian ở Pháp, có dạo tàu nằm sửa… Vậy là sau chặng đầu, Người đã ra được tới nước ngoài,…` → `Hồi ở Sài Gòn, Người từng nói muốn sang xem nước Pháp và các nước khác làm thế nào, rồi về giúp đồng bào. Tới Marseille đầu tháng 7/1911, Người vẫn chỉ là phụ bếp làm thuê cho hãng Năm Sao. Muốn xem cho tận tường thì phải được học, nên ở đất Pháp được hơn hai tháng, Người viết tay một lá đơn bằng tiếng Pháp,… Thư đi chừng một tháng thì có hồi âm, mà hồi âm là lời từ chối. Lý do nằm ở thủ tục:… Thành ra người dân thuộc địa muốn học cái hay của nước Pháp thì trước hết phải xin phép kẻ đang cai trị mình. Không vào được trường, Người vẫn làm thuê như cũ.… Lớp học không mở cửa, thì những bến cảng sẽ thành chỗ Người học.` [direction approved; full text SKILL § Mạch kể]

Do not copy from these books: self-certifying lines (`một tiểu sử trung thành, đúng đắn, sinh động, không thêu dệt`), period words in the narrator's own voice (`Nước Mẹ Đại Pháp`, `bônsêvích`, `vui thú lâm tuyền`), slogans and ready-made verdicts (`sung sướng ngất trời`, `ào ạt tiến lên`), absolute praise (`không bao giờ cãi cọ với ai`), serial "chờ xem kỳ sau" hooks, and long glosses wedged into a sentence. Both books tell the story in a third or first person close to Người; our narrator stays calm and outside, and invents no dialogue, sound or feeling that no source records.
