# Dựng RAG cho viet-tu-nhien

RAG ở đây chỉ là chỉ mục SQLite nằm ngay trong repo. Có bản nháp rồi thì agent tra chỉ mục này. Với từng câu, chỉ mục trả về các mẫu câu dịch đang dính, những cặp câu đã sửa, cách người Việt gọi ý ấy, từ nối và đoạn trích của người viết bản ngữ. RAG có hai lớp:

- Lớp từ khóa (SQLite FTS5) chỉ cần Python 3, không phải cài gì thêm.
- Lớp vector (model `gte-multilingual-base`, chạy trên CPU) giúp tìm theo nghĩa: bản nháp viết "giải phóng đất nước" vẫn tìm ra mục "cứu nước". Lớp này cần 5 gói Python và một model 341 MB.

Thiếu lớp vector thì lệnh vẫn chạy, chỉ tự lùi về từ khóa và ghi lý do ở dòng đầu kết quả.

Mọi lệnh dưới đây chạy từ thư mục gốc của repo.

## 1. Kiểm tra Python

```bash
python3 -c "import sqlite3; sqlite3.connect(':memory:').execute('create virtual table t using fts5(x)'); print('FTS5 ok')"
```

Lệnh này báo lỗi nghĩa là bản Python không có FTS5, cần cài bản Python khác (python.org, Homebrew, uv, hay bản của distro đều có).

## 2. Chỉ dùng từ khóa

```bash
python3 rag/build.py --stats
python3 rag/viet_rag.py search "cứu nước" -k 5 --mode keyword
```

`build.py` đọc `references/`, `evals/user-flagged.md` và `references/corpus/`, rồi ghi ra `rag/viet.db` (khoảng 1 MB, không đưa lên git). Sau đó không cần chạy lại bằng tay: `viet_rag.py` tự dựng lại chỉ mục mỗi khi có file nguồn mới hơn.

## 3. Thêm lớp vector

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python rag/build.py --vectors --stats
```

`--vectors` tải model từ Hugging Face về `rag/models/gte-multilingual-base/` (341 MB, không đưa lên git) rồi tính vector cho mọi mục, ghi vào `rag/viet_vec.db` (khoảng 3 MB). Lần đầu mất khoảng 45 giây và tốn khoảng 1.1 GB RAM. Những lần sau chỉ tính lại mục nào đổi chữ, mất chừng 2 giây. Hugging Face có in cảnh báo thiếu `HF_TOKEN` thì cứ bỏ qua, model này tải công khai được.

Dùng venv thì gọi đúng Python của venv: `.venv/bin/python rag/viet_rag.py …`. Các lệnh trong `SKILL.md` gọi `python3`. Nếu `python3` của agent không có các gói trên, kết quả sẽ ghi `retrieval keyword only (vector layer off: python module … not installed)`. Lúc đó chọn một trong hai cách: cài gói vào chính `python3` mà agent gọi, hoặc sửa lệnh trong `SKILL.md` sang `.venv/bin/python`.

Dựng vector và tra vector phải dùng cùng một bản onnxruntime. Dựng bằng 1.31 mà tra bằng 1.28 thì bài test theo nghĩa tụt từ 7/8 xuống 6/8. Đổi phiên bản rồi thì xóa `rag/viet_vec.db` và dựng lại.

## 4. Chạy thử

```bash
.venv/bin/python rag/viet_rag.py --selftest
.venv/bin/python scripts/viet_scan.py --selftest
```

Kết quả đo trên một bản clone mới (2026-10-28, Python 3.14, onnxruntime 1.31.1):

```
keyword  hit@3 = 11/11 · meaning-only 0/8
vector   hit@3 = 11/11 · meaning-only 7/8
hybrid   hit@3 = 11/11 · meaning-only 6/8
```

11 truy vấn đầu kiểm tra tìm theo chữ. 8 câu sau không có cặp âm tiết nào trùng với mục cần tìm, nên lớp từ khóa được 0/8 là đúng. Lệch một câu so với bảng trên thì chưa đáng lo. Máy quét phải ra `recall on bad, expected id: 101/101`.

## 5. Dùng

```bash
# Gói tham khảo cho từng câu của bản nháp (file, hoặc - để đọc từ stdin)
.venv/bin/python rag/viet_rag.py ref draft.md --register chat
printf '%s' "$TEXT" | .venv/bin/python rag/viet_rag.py ref - --register doc

# Tra một cụm, lọc theo loại
.venv/bin/python rag/viet_rag.py search "đóng vai trò" -k 5
.venv/bin/python rag/viet_rag.py search "mật thám" --kind naming,excerpt
```

| tùy chọn | dùng để |
|---|---|
| `--register narration\|chat\|doc` | chọn register, vừa để quét vừa để lọc mục hợp register (mặc định `narration`) |
| `--mode keyword\|vector\|hybrid` | cách tìm, mặc định `hybrid` |
| `-k N` | số kết quả của `search` |
| `--kind a,b` | lọc loại mục: `pattern`, `pair`, `keep`, `overcorrection`, `excerpt`, `naming`, `avoid`, `connective`, `user_flag` |
| `--per-sentence N` | số mục tối đa dưới mỗi câu trong `ref` (mặc định 3) |
| `--max-chars N` | độ dài tối đa của cả gói `ref` (mặc định 6000); gói dài hơn thì tự rút gọn |

Gói `ref` xếp theo thứ tự: mẫu câu máy quét bắt được (kèm cặp câu thật gần nhất), câu người đọc đã chê, cặp câu, cách gọi, từ nối, đoạn trích. Agent lấy cách nối câu và cách gọi tên trong gói, không chép dữ kiện hay giọng thời cũ của đoạn trích.

## Thêm nguồn

Mỗi nguồn mới để riêng một file `references/corpus/<tên>.jsonl`, mỗi dòng một object JSON:

```json
{"id": "TEN-NGUON-01", "kind": "excerpt", "text": "Đoạn trích nguyên văn…", "source": "Tác giả, tên sách hoặc kênh", "url": "https://…", "register": "narration", "tags": ["device:time-join"], "note": "Học được gì từ đoạn này."}
```

| trường | bắt buộc | ghi chú |
|---|---|---|
| `id` | có | không được trùng trong toàn bộ chỉ mục; nên đặt tiền tố theo nguồn |
| `kind` | nên có | `excerpt`, `pair`, `naming`, `avoid`, `connective`, `keep`, `overcorrection`; bỏ trống hoặc ghi loại khác (ví dụ `rule`) thì được tính là `excerpt` |
| `text` | có | chép nguyên văn, không sửa chữ |
| `source`, `url` | có | để người sau kiểm lại và để chủ sở hữu yêu cầu gỡ được |
| `register` | nên có | `narration`, `chat`, `doc`, `formal`, `memoir`; bỏ trống là hợp mọi register |
| `tags`, `note` | không | cũng được đưa vào chỉ mục; mã mẫu câu trong đó (ví dụ `B01`) nối mục với mẫu câu ấy |

Với cặp câu, ghi `"kind": "pair"` kèm hai trường `"bad"` và `"natural"`, hoặc viết `text` dạng `câu xấu → câu tốt`.

Thêm xong thì kiểm tra:

```bash
.venv/bin/python rag/build.py --stats                     # tổng số mục phải tăng; dòng JSON hỏng sẽ bị bỏ qua và báo "skip …"
.venv/bin/python rag/viet_rag.py search "<một cụm trong đoạn mới>" -k 3
.venv/bin/python rag/viet_rag.py --selftest               # không được tụt so với trước
```

Đoạn trích đưa vào là để agent học cách người Việt nối câu và gọi tên sự việc, nên trước khi thêm hãy chạy máy quét trên từng đoạn (`scripts/viet_scan.py - --register <register>`). Đoạn nào bị bắt mà vẫn giữ thì ghi lý do vào `note`.

## Sự cố thường gặp

| thấy | làm |
|---|---|
| `vector layer off: python module X not installed` | cài `requirements.txt` vào đúng Python đang gọi |
| `model not downloaded` | chạy `build.py --vectors` |
| `vector DB refresh failed: …` | xóa `rag/viet_vec.db`, chạy lại `build.py --vectors` |
| `AttributeError: … enable_load_extension` | bản Python không cho nạp extension SQLite, sqlite-vec cần quyền này; đổi sang bản Python khác (Homebrew, uv, python.org) |
| kết quả cũ dù đã sửa file nguồn | xóa `rag/viet.db` và `rag/viet_vec.db`, dựng lại |
| bị kill khi dựng vector | máy thiếu RAM; cần khoảng 1.1 GB trống, hoặc tạm dùng `--mode keyword` |
