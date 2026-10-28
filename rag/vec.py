"""Semantic layer of the viet-tu-nhien RAG: unit embeddings in rag/viet_vec.db (sqlite-vec).

Model: onnx-community/gte-multilingual-base, int8 ONNX (340 MB), CLS pooling, 768 dims, run on CPU with
onnxruntime + tokenizers. Cached in rag/models/ (a download, not source). viet_vec.db maps each unit uid
to its vector; a refresh re-embeds only units whose embedded text changed. Built by `rag/build.py --vectors`;
viet_rag.py refreshes it when viet.db is newer.
"""
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

RAG = Path(__file__).resolve().parent
sys.path.insert(0, str(RAG))
import build  # noqa: E402

REPO = 'onnx-community/gte-multilingual-base'
NAME = REPO.split('/')[1]
MODEL_DIR = RAG / 'models' / NAME
FILES = ('onnx/model_int8.onnx', 'tokenizer.json', 'config.json')
ONNX, TOKENIZER = MODEL_DIR / FILES[0], MODEL_DIR / FILES[1]
DIM = 768
MAX_TOKENS = 256
VDB = RAG / 'viet_vec.db'
CODES = re.compile(r'\s*\((?:[0-9]*[A-Z]+\d{2}(?:,\s*)?)+\)|\s*\[[^\]]*#\d+\]')  # "(B01, C02)", "[r4 …, #2]"


# ---------- availability ----------

def missing_libs():
    try:
        import numpy  # noqa: F401
        import onnxruntime  # noqa: F401
        import sqlite_vec  # noqa: F401
        import tokenizers  # noqa: F401
    except ImportError as e:
        return f'python module {e.name} not installed'
    return ''


def have_model():
    return ONNX.exists() and TOKENIZER.exists()


def stale(db=build.DB, vdb=VDB):
    if not vdb.exists():
        return True
    t = vdb.stat().st_mtime
    return any(p.exists() and p.stat().st_mtime > t for p in (db, Path(__file__), ONNX))


def unavailable(db=build.DB, vdb=VDB):
    """Why the vector layer cannot be used right now ('' when it can). Refreshes a stale viet_vec.db."""
    why = missing_libs()
    if why:
        return why
    if not have_model():
        return f'model not downloaded (python3 rag/build.py --vectors → rag/models/{NAME})'
    if stale(db, vdb):
        try:
            refresh(db, vdb)
        except Exception as e:  # keep keyword search working whatever went wrong here
            return f'vector DB refresh failed: {type(e).__name__}: {e}'
    return ''


def download():
    from huggingface_hub import hf_hub_download
    for f in FILES:
        hf_hub_download(REPO, f, local_dir=MODEL_DIR)
    return MODEL_DIR


# ---------- embedding ----------

def embed_text(u):
    """What gets embedded for one unit: its text (a pair as `bad → natural`), the English concept of a
    naming row, the note; source codes stripped."""
    t = u['t'].replace(' | ', ' → ', 1) if u['kind'] in ('pair', 'overcorrection') else u['t']
    parts = [t]
    if u['kind'] == 'naming':
        parts.append(json.loads(u['extra'] or '{}').get('concept', ''))
    if u['note'] and u['note'] not in u['t']:
        parts.append(u['note'])
    return CODES.sub('', ' — '.join(p for p in parts if p)[:600])


_MODEL = None


def model():
    """(onnx session, tokenizer), loaded once per process."""
    global _MODEL
    if _MODEL is None:
        import onnxruntime as ort
        from tokenizers import Tokenizer
        so = ort.SessionOptions()
        so.intra_op_num_threads = min(4, os.cpu_count() or 1)
        so.log_severity_level = 3
        sess = ort.InferenceSession(str(ONNX), so, providers=['CPUExecutionProvider'])
        tok = Tokenizer.from_file(str(TOKENIZER))
        tok.enable_truncation(MAX_TOKENS)
        tok.enable_padding()
        _MODEL = sess, tok
    return _MODEL


def embed(texts, batch=16):
    """L2-normalised float32 vectors (len(texts) × DIM), CLS pooling."""
    import numpy as np
    sess, tok = model()
    out = []
    for i in range(0, len(texts), batch):
        enc = tok.encode_batch([build.nfc(t) for t in texts[i:i + batch]])
        ids = np.array([e.ids for e in enc], dtype=np.int64)
        mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
        cls = sess.run(None, {'input_ids': ids, 'attention_mask': mask})[0][:, 0]
        out.append(cls / np.linalg.norm(cls, axis=1, keepdims=True))
    return np.vstack(out).astype(np.float32) if out else np.zeros((0, DIM), np.float32)


# ---------- store ----------

def connect(vdb=VDB):
    import sqlite_vec
    con = sqlite3.connect(vdb)
    con.enable_load_extension(True)
    sqlite_vec.load(con)
    con.enable_load_extension(False)
    return con


VSCHEMA = f"""
CREATE TABLE info(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE meta(id INTEGER PRIMARY KEY, uid TEXT UNIQUE, h TEXT);
CREATE VIRTUAL TABLE vec USING vec0(embedding float[{DIM}] distance_metric=cosine);
"""


def refresh(db=build.DB, vdb=VDB, log=None):
    """Rebuild viet_vec.db from viet.db, reusing vectors of units whose embedded text is unchanged.
    Returns (units, newly embedded, seconds)."""
    t0 = time.time()
    src = sqlite3.connect(db)
    src.row_factory = sqlite3.Row
    units = [dict(r) for r in src.execute('SELECT id, uid, kind, t, note, extra FROM units ORDER BY id')]
    src.close()
    texts = [embed_text(u) for u in units]
    hashes = [hashlib.sha1(f'{NAME}\n{MAX_TOKENS}\n{t}'.encode()).hexdigest() for t in texts]
    old = {}
    if vdb.exists():
        try:
            oc = connect(vdb)
            old = dict(oc.execute('SELECT m.h, v.embedding FROM meta m JOIN vec v ON v.rowid = m.id'))
            oc.close()
        except sqlite3.Error:
            old = {}
    todo = [i for i, h in enumerate(hashes) if h not in old]
    if log and todo:
        log(f'embedding {len(todo)} of {len(units)} units with {NAME}…')
    fresh = dict(zip((hashes[i] for i in todo), embed([texts[i] for i in todo]))) if todo else {}
    tmp = vdb.with_name(f'{vdb.stem}.tmp{os.getpid()}')
    tmp.unlink(missing_ok=True)
    con = connect(tmp)
    con.executescript(VSCHEMA)
    con.executemany('INSERT INTO info VALUES (?, ?)', [('model', REPO), ('file', FILES[0]), ('dim', str(DIM))])
    for u, h in zip(units, hashes):
        v = fresh[h].tobytes() if h in fresh else old[h]
        con.execute('INSERT INTO meta VALUES (?, ?, ?)', (u['id'], u['uid'], h))
        con.execute('INSERT INTO vec(rowid, embedding) VALUES (?, ?)', (u['id'], v))
    con.commit()
    con.execute('VACUUM')
    con.close()
    tmp.replace(vdb)
    return len(units), len(todo), time.time() - t0


def knn(vcon, qvec, k=40):
    """[(uid, cosine similarity)] of the k nearest units, best first."""
    rows = vcon.execute('SELECT m.uid, v.distance FROM vec v JOIN meta m ON m.id = v.rowid '
                        'WHERE v.embedding MATCH ? AND k = ? ORDER BY v.distance', (qvec.tobytes(), k))
    return [(uid, 1.0 - d) for uid, d in rows]

