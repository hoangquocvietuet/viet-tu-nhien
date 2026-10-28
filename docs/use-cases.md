# Dùng skill cho từng loại văn bản

Loại nào cũng đi cùng một quy trình trong `SKILL.md`: chốt dữ kiện, kể lại bằng tiếng Việt, tra RAG, viết lại, soát từng đoạn. Khác nhau ở register và ở những mẫu câu hay lộ ra. Máy quét có ba register: `chat`, `doc`, `narration`. Văn bản trang trọng dùng `doc`.

Ví dụ nào ghi **(minh họa)** là câu viết ra để minh họa. Ví dụ không ghi là cặp câu có thật, lấy từ `references/pairs.md`. Mã như `C01`, `F05` là id trong `references/patterns.md`.

## Trả lời chat, báo cáo tiến độ, kế hoạch

Register `chat`. Viết như nhắn cho đồng nghiệp: ai làm gì, xong chưa, cần người kia quyết gì. Hay lộ ở chỗ dòng trạng thái lấy quá trình làm chủ ngữ (G03), danh sách nhãn in đậm (G01), câu mở "Dưới đây là" (F05), và câu hỏi duyệt cộc lốc kiểu "Giữ, hay né?" (G05). Thuật ngữ người dùng hay nói (render, commit, deploy) cứ để nguyên. Xưng hô theo đúng cách người dùng xưng.

- `Dàn ý tập 1 đã xong và đã qua hai lượt phản biện chéo (Grok và GPT), bạn duyệt giúp trước khi mình cho viết lời.` → `Dàn ý tập 1 xong rồi, Grok với GPT đã đọc chéo hai lượt. Bạn xem giúp, ổn thì mình cho viết lời.`
- `Việc cập nhật cấu hình đã được thực hiện thành công.` → `Mình cập nhật cấu hình xong rồi.` **(minh họa)**

```bash
python3 scripts/viet_scan.py reply.md --register chat
```

## README, tài liệu kỹ thuật, ghi chú

Register `doc`. Tài liệu được dùng tiêu đề, được danh từ hóa một ít cho thuật ngữ, thỉnh thoảng có "tuy nhiên". Cái cần bỏ là thành ngữ dịch ("đóng vai trò", E01), chuỗi "của" (B09), "nó" chỉ đồ vật (B05), và câu mở nói về chính bài viết ("Trong bài viết này, chúng ta sẽ cùng tìm hiểu…", F05).

- `Trong bài viết này, chúng ta sẽ cùng tìm hiểu cách Redis lưu dữ liệu…` → `Redis lưu dữ liệu thường dùng trong bộ nhớ, nhờ đó hệ thống ít phải truy cập nguồn dữ liệu chậm hơn.`
- `Nếu file đã bị thay đổi kể từ lúc tải, endpoint trả về lỗi 409.` → `Nếu file đã đổi từ lúc được tải lên màn hình, endpoint trả 409 và không ghi gì.`

```bash
python3 scripts/viet_scan.py README.md --register doc
python3 rag/viet_rag.py ref README.md --register doc
```

## Commit message, mô tả PR

Register `doc`. Dòng đầu bắt đầu bằng động từ và nói việc đã làm. Đừng đặt "việc" trước động từ (D01), đừng dùng động từ đệm như "thực hiện", "tiến hành" (D02).

- `Thực hiện việc sửa lỗi liên quan đến chức năng đăng nhập` → `Sửa lỗi đăng nhập khi mật khẩu có dấu cách` **(minh họa)**

## Dịch từ tiếng Anh

Chọn register theo bản đích. Đây là chỗ dễ lộ nhất, vì câu tiếng Anh nằm sẵn trước mắt và thành luôn bộ khung cho câu tiếng Việt. Làm theo § English sources trong `SKILL.md`: đọc bản tiếng Anh, gấp lại, ghi dữ kiện bằng tiếng Việt theo lời mình, rồi viết từ danh sách đó. Chỉ mở lại bản gốc để đối chiếu dữ kiện. Thứ tự gạch đầu dòng trong bản gốc không phải thứ tự kể.

- *bring them the benefits of instruction*: `và đem lại cho họ những lợi ích của việc học.` → `rồi đem sự học ấy về cho họ.`
- *This feature allows users to export their data with a single click.*: `Tính năng này cho phép người dùng xuất dữ liệu của họ với một cú nhấp chuột duy nhất.` → `Chỉ cần bấm một lần là xuất được dữ liệu.` **(minh họa)**

Riêng trích dẫn thì không kể lại. Lời trích phải giữ nguyên chữ, thấy khó hiểu thì thêm một câu giải thích ở trước hoặc sau.

## Email, thư công việc, văn bản hành chính

Register `doc` (bảng register trong `SKILL.md` gọi là `formal`). Ở đây được dùng Hán Việt, được dùng bị động khi văn bản cố ý không nêu người làm. Cần bỏ câu mở dịch từ "I am writing to inform you that…" và các khung dịch như "đóng vai trò", "có số phận".

- `Tôi viết email này để thông báo rằng cuộc họp đã được dời sang thứ Năm.` → `Xin báo để anh chị biết: cuộc họp dời sang thứ Năm.` **(minh họa)**

## Chữ trên giao diện, thông báo lỗi

Register `doc`. Câu ngắn, nói cho người dùng biết chuyện gì vừa xảy ra và giờ làm gì. Tránh câu bị động không có người làm (C01) và chữ "của bạn" dịch từ "your" ở chỗ không cần.

- `Đã xảy ra lỗi trong quá trình xử lý yêu cầu của bạn.` → `Chưa lưu được thay đổi. Bạn thử lại sau ít phút.` **(minh họa)**

Chuỗi giao diện thường chỉ dài một câu, nên gom nhiều chuỗi vào chung một file, mỗi chuỗi một đoạn (cách nhau một dòng trống), rồi quét một lần.

## Mô tả sản phẩm, nội dung marketing

Register `doc`. Văn quảng cáo dịch hay mắc "không chỉ… mà còn" chỉ để tạo nhịp (E05), và tính từ chung chung thay cho dữ kiện. Một con số cụ thể có sức nặng hơn ba tính từ.

- `Không chỉ giúp tỉnh táo, cà phê mà còn mang lại nhiều lợi ích cho sức khỏe.` → `Một ly cà phê buổi sáng giúp tỉnh người nhanh.`
- `Việc quản lý trở nên dễ dàng hơn.` → `Báo cáo tuần giờ có trong 15 phút thay vì cả buổi chiều.`

## Bài mạng xã hội, caption

Bài nói chuyện với người đọc thì dùng `chat`, bài mô tả thì dùng `doc`. Câu mở kiểu chatbot ("Hãy cùng khám phá…", "Bạn đã bao giờ…?") lộ ra ngay từ dòng đầu.

- `Hãy cùng khám phá những lợi ích tuyệt vời này nhé!` → `Caffeine ngấm vào máu chỉ sau vài phút và rõ nhất sau khoảng một tiếng.`
- `Chắc chắn rồi! Trong thời đại 4.0 ngày nay, AI không chỉ là một công cụ mà còn là người bạn đồng hành…` → `Phòng tôi bắt đầu dùng AI từ tháng trước, chủ yếu để soạn email và tóm tắt biên bản họp.`

## Lời thuyết minh, kịch bản video, podcast

Register `narration`. Người nghe chỉ nghe một lần, không đọc lại được. Đây là phần skill viết kỹ nhất: § Mạch kể (câu sau trả lời câu hỏi câu trước để lại, có gọi lại chi tiết cũ, từ nối theo đúng quan hệ), bước 2b (lập mạch ý rồi mới viết nháp), bước 5b (đọc cả đoạn). Review từng đoạn một, đừng review cả kịch bản trong một lượt. Kịch bản đọc bằng TTS thì viết số, đơn vị và ký hiệu ra thành chữ, theo cách người đọc sẽ nói.

- `Câu ông nói được Toàn thư ghi lại thế này:` → `Toàn thư chép lại câu ông nói thế này:`
- `hơn bảy trăm năm, lâu hơn Tây Đô rất nhiều.` → `hơn bảy trăm năm, Tây Đô làm sao bì được.`

```bash
python3 scripts/viet_scan.py script.md --register narration
python3 rag/viet_rag.py ref script.md --register narration
```

## Tiêu đề

Tiêu đề nên đọc như lời người kể chuyện, không như một nhãn dịch. Quét tiêu đề cùng register với phần thân.

- `Cái gì giữ một kinh đô` → `Không phải nhờ bức tường`
- `Hơn chục kinh đô, hai kiểu` → `Hơn chục nơi từng làm kinh đô`

## Khi nào không nên sửa

Loại văn bản nào cũng vậy: máy quét báo ít đi chưa chắc câu đã tự nhiên hơn. "bị/được" đúng nghĩa thiệt hay lợi, loại từ ("một tờ chiếu"), "là" trong câu định danh, Hán Việt chuyên ngành, các câu rào đón như "tôi đoán", "có lẽ" đều phải giữ. Danh sách đầy đủ ở § Do not over-correct trong `SKILL.md` và mục "Giữ nguyên" trong `references/pairs.md`.
