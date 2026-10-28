# viet-tu-nhien

Skill cho agent AI (Claude Code, Codex và các agent đọc được `SKILL.md`) để viết tiếng Việt như người Việt nói, không phải tiếng Anh dịch từng chữ.

Câu "Cái gì giữ một kinh đô" không có chữ tiếng Anh nào, vậy mà người Việt nghe là biết dịch từ "What keeps a capital". Cái lộ ra là bộ khung câu: chủ ngữ trừu tượng, "một" dùng như mạo từ, "nó" để chỉ đồ vật, bị động giấu người làm, chuỗi "của". Skill này dạy agent kể lại từ dữ kiện thay vì dịch. Đi kèm có danh mục 66 mẫu câu dịch, hơn 150 cặp câu gốc và câu đã sửa (lấy từ bản sửa thật, không bịa), một máy quét để soát nhanh và một RAG chạy ngay trên máy để tra khi viết lại.

## Dùng cho việc gì

Văn bản tiếng Việt nào cũng dùng được: trả lời chat, báo cáo tiến độ, README, commit và PR, email, chữ trên giao diện, mô tả sản phẩm, bài mạng xã hội, lời thuyết minh video hay podcast, và mọi bản dịch sang tiếng Việt. Mỗi loại cần chọn register nào, soát chỗ nào, chạy lệnh gì thì xem [`docs/use-cases.md`](docs/use-cases.md).

## Cài vào agent

```bash
git clone https://github.com/hoangquocvietuet/viet-tu-nhien ~/.agents/skills/viet-tu-nhien
mkdir -p ~/.claude/skills && ln -s ~/.agents/skills/viet-tu-nhien ~/.claude/skills/viet-tu-nhien   # Claude Code
```

Các lệnh trong `SKILL.md` gọi theo đường dẫn `~/.agents/skills/viet-tu-nhien`. Clone ra chỗ khác thì tạo symlink về đúng chỗ đó.

Máy quét và tìm theo từ khóa chỉ cần Python 3 có SQLite FTS5 (bản Python thông thường đều có; repo đã chạy thử trên 3.14). Muốn tìm theo nghĩa thì cài thêm lớp vector, xem [`docs/rag-setup.md`](docs/rag-setup.md).

## Dùng nhanh

```bash
cd ~/.agents/skills/viet-tu-nhien

# Soát một bản nháp: cue chỉ báo câu nên đọc lại, không phải lỗi chắc chắn
python3 scripts/viet_scan.py draft.md --register chat
printf '%s' "Dưới đây là kế hoạch chi tiết cho việc triển khai tính năng mới." | python3 scripts/viet_scan.py - --register chat

# Lấy gói tham khảo cho từng câu trong bản nháp rồi viết lại
python3 rag/viet_rag.py ref draft.md --register doc

# Tra một ý
python3 rag/viet_rag.py search "cứu nước" -k 5
```

Thứ tự làm việc mà skill hướng dẫn agent: lập mạch ý, viết nháp, tra RAG, viết lại, rồi review từng đoạn nhỏ. Chi tiết nằm trong [`SKILL.md`](SKILL.md).

## Trong repo có gì

```
SKILL.md                    quy trình cho agent: register, kể lại từ dữ kiện, mạch kể, chống sửa quá tay
references/patterns.md      66 mẫu câu dịch (A–G), mỗi mẫu có gốc tiếng Anh, cặp câu thật, cách nhận ra
references/pairs.md         các cặp câu trước → sau, danh sách "Giữ nguyên", những lần sửa quá tay
references/connectives.md   từ nối xếp theo quan hệ: thêm ý, nói rõ, thời gian, nhân quả, đảo ý, điều kiện, chốt
references/cach-goi.md      cách người Việt gọi các ý lớn (độc lập, bế tắc, bước ngoặt...) thay cho cụm tự đặt
references/corpus/          đoạn trích nguyên văn của người viết tiếng Việt, có URL nguồn
evals/user-flagged.md       những câu người đọc bản ngữ đã chê, dùng làm bộ test sau mỗi lần sửa skill
scripts/viet_scan.py        máy quét (chỉ dùng thư viện chuẩn, không tự sửa chữ, luôn thoát 0)
rag/                        chỉ mục SQLite FTS5 + vector (sqlite-vec, gte-multilingual-base)
docs/                       hướng dẫn theo loại văn bản và cách dựng RAG
```

## Sửa xong thì kiểm tra

```bash
python3 scripts/viet_scan.py --selftest   # recall trên câu xấu, báo nhầm trên câu tốt
python3 rag/viet_rag.py --selftest        # hit@3 cho 11 truy vấn theo chữ và 8 câu chỉ giống về nghĩa
```

Hai bài selftest chỉ để bắt lỗi lùi. Regex được viết khi đã nhìn thấy các cặp câu ấy, nên con số không nói được độ chính xác trên văn bản mới. Câu nào tự nhiên hay không thì người đọc bản ngữ quyết, điểm số của model không thay được.

## Thêm nguồn

Repo sẽ còn thêm nhiều nguồn. Mỗi nguồn để riêng một file `references/corpus/<tên>.jsonl`, mỗi dòng một đoạn trích. Lần chạy RAG sau sẽ tự đưa file mới vào chỉ mục. Định dạng và các bước kiểm tra nằm ở [`docs/rag-setup.md`](docs/rag-setup.md#thêm-nguồn). Cặp câu thêm vào `references/pairs.md` phải là bản sửa có thật, ghi rõ nguồn; câu tự viết để minh họa thì đánh dấu **(minh họa)**.

## Nguồn và bản quyền

Code và phần chữ viết cho repo này theo giấy phép MIT (`LICENSE`). Đoạn trích trong `references/corpus/` được chép nguyên văn từ các bài viết, sách và video công khai, mỗi đoạn có URL gốc, và vẫn thuộc về tác giả. Đoạn nào chủ sở hữu muốn gỡ, xin mở issue.
