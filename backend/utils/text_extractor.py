import os
import PyPDF2
import docx


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_pdf(file_path)
    elif ext == ".docx":
        return _extract_docx(file_path)
    elif ext == ".txt":
        return _extract_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _extract_pdf(path: str) -> str:
    text = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(f"\nPAGE_BREAK\n{page_text.strip()}")
    return "\n\n".join(text)


def _extract_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())


def _extract_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def chunk_text(text: str, chunk_size: int = 250, overlap: int = 60):
    """
    Paragraph-aware chunking for better RAG retrieval.
    """

    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]

    chunks = []
    current_chunk = []
    current_words = 0

    for para in paragraphs:
        para_words = para.split()

        if len(para_words) > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_words = 0

            start = 0
            while start < len(para_words):
                end = start + chunk_size
                piece = " ".join(para_words[start:end])
                chunks.append(piece)
                start += chunk_size - overlap

            continue

        # Add paragraph to current chunk if fits
        if current_words + len(para_words) <= chunk_size:
            current_chunk.append(para)
            current_words += len(para_words)

        else:
            chunks.append(" ".join(current_chunk))

            # overlap from previous chunk
            prev_words = " ".join(current_chunk).split()
            overlap_words = prev_words[-min(overlap, len(prev_words)):]

            current_chunk = [
                " ".join(overlap_words),
                para
            ]
            current_words = len(overlap_words)+len(para_words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks