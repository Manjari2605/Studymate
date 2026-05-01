import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.database import get_db, Note, Chunk
from backend.utils.text_extractor import extract_text, chunk_text
from backend.services.vector_store import add_chunks, delete_chunks

router = APIRouter(prefix="/notes", tags=["notes"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}


@router.post("/upload")
async def upload_note(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a note file, extract text, chunk it, and index in FAISS."""

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Use PDF, TXT, or DOCX.")

    # Save file to disk
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
        f.flush()
        os.fsync(f.fileno())

    file_size_bytes = os.path.getsize(save_path)
    file_size_str   = f"{round(file_size_bytes / 1024, 1)} KB" if file_size_bytes < 1024*1024 else f"{round(file_size_bytes / (1024*1024), 1)} MB"

    # Extract text
    try:
        text = extract_text(save_path)
    except Exception as e:
        os.remove(save_path)
        raise HTTPException(status_code=422, detail=f"Could not extract text: {str(e)}")

    if not text.strip():
        raise HTTPException(status_code=422, detail="File appears to be empty or unreadable.")

    # Guess subject from filename
    name_lower = file.filename.lower()
    subject    = "General"
    for s in ["biology", "physics", "chemistry", "maths", "math", "history", "english", "computer"]:
        if s in name_lower:
            subject = s.capitalize()
            break

    # Save note to DB
    note = Note(filename=file.filename, subject=subject, content=text, file_size=file_size_str)
    db.add(note)
    db.commit()
    db.refresh(note)

    # Chunk and index
    chunks   = chunk_text(text)
    faiss_ids = add_chunks(chunks)

    for chunk_text_val, fid in zip(chunks, faiss_ids):
        db.add(Chunk(note_id=note.id, text=chunk_text_val, faiss_id=fid))
    db.commit()

    return {
        "message":  "Note uploaded and indexed successfully.",
        "note_id":  note.id,
        "filename": note.filename,
        "subject":  note.subject,
        "chunks":   len(chunks),
        "size":     file_size_str,
    }


@router.get("/")
def list_notes(db: Session = Depends(get_db)):
    """Return all uploaded notes."""
    notes = db.query(Note).order_by(Note.created_at.desc()).all()
    return [
        {
            "id":         n.id,
            "filename":   n.filename,
            "subject":    n.subject,
            "file_size":  n.file_size,
            "created_at": n.created_at.strftime("%d %b %Y, %I:%M %p"),
        }
        for n in notes
    ]


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note and remove its chunks from FAISS."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")

    # Get faiss ids to remove
    chunks    = db.query(Chunk).filter(Chunk.note_id == note_id).all()
    faiss_ids = [c.faiss_id for c in chunks]

    # Delete from FAISS
    delete_chunks(faiss_ids)

    # Delete from DB
    db.query(Chunk).filter(Chunk.note_id == note_id).delete()
    db.delete(note)
    db.commit()

    # Delete file from disk
    file_path = os.path.join(UPLOAD_DIR, note.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"message": f"Note '{note.filename}' deleted successfully."}