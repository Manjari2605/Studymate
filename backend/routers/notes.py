import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.database import get_db, Note

from backend.utils.text_extractor import extract_text

router = APIRouter(prefix="/notes", tags=["notes"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}


@router.post("/upload")
async def upload_note(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    save_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        text = extract_text(save_path)
    except Exception as e:
        os.remove(save_path)
        raise HTTPException(status_code=422, detail=str(e))

    if not text.strip():
        raise HTTPException(status_code=422, detail="Empty file")

    note = Note(
        filename=file.filename,
        subject="General",
        content=text,
        file_size=str(os.path.getsize(save_path))
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return {"message": "Uploaded successfully", "note_id": note.id}


@router.get("/")
def list_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(note)
    db.commit()

    return {"message": "Deleted"}