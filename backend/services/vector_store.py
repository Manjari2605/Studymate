import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

INDEX_PATH    = "data/index/faiss.index"
META_PATH     = "data/index/meta.pkl"
EMBED_MODEL   = "sentence-transformers/all-MiniLM-L6-v2"
DIMENSION     = 384

embedder = SentenceTransformer(EMBED_MODEL)


def _load_index():
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            meta = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(DIMENSION)
        meta  = []  
    return index, meta


def _save_index(index, meta):
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(meta, f)


def add_chunks(chunks: list[str]) -> list[int]:
    """Embed chunks and add to FAISS. Returns list of faiss IDs assigned."""
    index, meta = _load_index()

    embeddings = embedder.encode(chunks, show_progress_bar=False)
    embeddings = np.array(embeddings, dtype="float32")

    start_id = len(meta)
    index.add(embeddings)
    meta.extend(chunks)

    _save_index(index, meta)

    faiss_ids = list(range(start_id, start_id + len(chunks)))
    return faiss_ids


def search(query: str, top_k: int = 3) -> list[str]:
    """Search FAISS for most relevant chunks to the query."""
    index, meta = _load_index()

    if index.ntotal == 0:
        return []

    query_vec = embedder.encode([query], show_progress_bar=False)
    query_vec = np.array(query_vec, dtype="float32")

    distances, indices = index.search(query_vec, min(top_k, index.ntotal))

    results = []
    for idx in indices[0]:
        if idx != -1 and idx < len(meta):
            results.append(meta[idx])

    return results


def delete_chunks(faiss_ids: list[int]):
    """
    FAISS FlatL2 does not support direct deletion.
    We rebuild the index excluding the given ids.
    """
    index, meta = _load_index()

    if index.ntotal == 0:
        return

    keep_ids = [i for i in range(len(meta)) if i not in faiss_ids]
    if not keep_ids:
        new_index = faiss.IndexFlatL2(DIMENSION)
        new_meta  = []
    else:
        kept_texts = [meta[i] for i in keep_ids]
        embeddings = embedder.encode(kept_texts, show_progress_bar=False)
        embeddings = np.array(embeddings, dtype="float32")
        new_index  = faiss.IndexFlatL2(DIMENSION)
        new_index.add(embeddings)
        new_meta = kept_texts

    _save_index(new_index, new_meta)


