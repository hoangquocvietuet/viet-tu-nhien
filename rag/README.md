# rag: retrieval for viet-tu-nhien (sqlite3 FTS5 + sqlite-vec)

`build.py` indexes `references/{pairs,patterns,cach-goi,connectives}.md`, `evals/user-flagged.md`, `references/corpus/*.md` and `*.jsonl` (research contract) into `viet.db`, one row per unit, each with a `file#anchor:line` pointer. `viet.db` is a build artifact. `viet_rag.py` rebuilds it when any source is newer, so new corpus files are picked up on their own. FTS5 uses `unicode61 remove_diacritics 0`, plus a hidden column of `a_b` syllable bigrams (weight 2.5) so phrases outrank single syllables. Stopwords are dropped from single-syllable terms only. `ref` also runs `scripts/viet_scan.py` (imported) per paragraph and puts each fired pattern, with its closest real pair, first.

```
python3 rag/build.py [--stats] [--vectors]        # from the repo root
python3 rag/viet_rag.py search "<text>" [--kind pair,user_flag] [-k 5] [--mode keyword|vector|hybrid]
python3 rag/viet_rag.py ref draft.md|- [--register narration|chat|doc] [--per-sentence 3] [--max-chars 6000] [--mode …]
python3 rag/viet_rag.py --selftest [--mode …]
```

Pack order per sentence: scanner hits, then strong matches by kind (user_flag, pair/pattern/keep/over-fix, naming/avoid, connective, excerpt), then weaker ones by score. Each unit appears once, under the sentence it shares wording with best (else the one it matches best). The pack shrinks (shorter lines, short pointers, fewer items) until it fits `--max-chars`.

## Vector layer (semantic search)

`vec.py` embeds every unit with **`onnx-community/gte-multilingual-base`** (int8 ONNX, 340 MB on disk, 768 dims, CLS pooling, Apache-2.0), run on CPU through `onnxruntime` + `tokenizers`, and stores the vectors in `viet_vec.db` (sqlite-vec `vec0`, cosine, 3.2 MB). What gets embedded: the unit text (a pair as `bad → natural`), the English concept of a naming row and the note, with source codes like `(B01, C02)` stripped.

- **Model cache:** `rag/models/gte-multilingual-base/` is a download, not source; keep it out of git (`rag/models/`, like `viet.db` and `viet_vec.db`). `python3 rag/build.py --vectors` fetches it (Hugging Face, about 10 s) and builds the vectors.
- **Rebuild:** `build.py` refreshes `viet_vec.db` whenever the model is present; `viet_rag.py` refreshes it on its own when `viet.db` (or `vec.py`, or the model) is newer. A refresh re-embeds only units whose embedded text changed (keyed by a hash): 3 changed units took 1.8 s including model load, an unchanged index 0.2 s. Full build: about 45 s for ~850 units, peak RSS 1.1 GB; on a shared box give it 2 GB.
- **Modes:** `keyword` = FTS5 bm25 only; `vector` = cosine only; `hybrid` = reciprocal rank fusion of the two top-40 lists, score = Σ 1000 / (10 + rank). Default is hybrid; if a Python module, the model or the vector DB is unavailable, the run falls back to keyword and says why in the pack header (`retrieval keyword only (vector layer off: …)`) or in the `retrieval:` line that ends `search`. Asking for `--mode vector|hybrid` without the layer is an error.
- **Downstream:** a hit with no shared content bigram still counts in `ref` when its similarity is within 0.05 of the sentence's best (0.025 to rank as strong); the bm25 tests for wording are unchanged. `search` lines add `sim=` when a vector score exists.
- **Candidates tried** (vector only, hit@3 on an earlier 8-sentence meaning probe, embedded text still carrying source codes): gte-multilingual-base int8 (340 MB) 5/8, 6/8 once the codes were stripped; bge-m3 int8 (568 MB, embeds 2.4× slower) 4/8; multilingual-e5-base int8 (278 MB) 3/8.
- **Install:** `requirements.txt` (numpy, onnxruntime, tokenizers, huggingface_hub, sqlite-vec); steps, troubleshooting and the corpus format are in `docs/rag-setup.md`. Build the vectors and query them with the same onnxruntime: vectors built under one version and queried under another scored 6/8 instead of 7/8 on the meaning probe.

## Acceptance run (fresh clone, 2026-10-28)

Python 3.14 venv from `requirements.txt`: numpy 2.5.4, onnxruntime 1.31.1, tokenizers 0.23.3, huggingface_hub 2.3.0, sqlite-vec 0.1.9.

```
$ .venv/bin/python rag/build.py --vectors --stats
excerpt 307 · pair 155 · naming 139 · pattern 67 · avoid 54 · connective 45 · keep 24 · user_flag 16 · overcorrection 8
total 815 · sources: 13 files (2 jsonl) · rag/viet.db: 932 KiB
built rag/viet_vec.db: 815 units, 815 embedded with gte-multilingual-base, 44.4 s · rag/viet_vec.db: 3208 KiB
peak RSS 1.1 GB; rag/models 341 MB

$ .venv/bin/python rag/viet_rag.py --selftest     # 11 wording queries; 8 sentences sharing no content bigram with their target
keyword  hit@3 = 11/11 · meaning-only 0/8
vector   hit@3 = 11/11 · meaning-only 7/8      # miss: "Đơn xin nhập học bị bác…" (E12 rows outrank A14/U08)
hybrid   hit@3 = 11/11 · meaning-only 6/8      # misses: "Người lên bờ ở xứ sở của người Pháp", "Sau biến cố đó, đời Người đổi khác"

$ .venv/bin/python rag/viet_rag.py search 'Đơn xin nhập học bị bác bằng một lý do giấy tờ khô khốc' -k 3
1. [pair] pair:E12.1  score=134.39 bigrams=0 sim=0.646
2. [pattern] pat:E12  score=123.33 bigrams=0 sim=0.618
3. [pattern] pat:A14  score=110.12 bigrams=0 sim=0.598
retrieval: hybrid (gte-multilingual-base)
```

An index built on 2026-10-27 from an earlier state of the references scored 8/8 (vector) and 7/8 (hybrid); rebuilt from scratch, the same files give 7/8 and 6/8, so treat one sentence either way as noise.

Still weak: plain fact sentences (dates, ship names, letters) keep pulling units that share a name or a number in either mode.
