from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.auth import current_user
from app.db import get_db
from app.models import Note as NoteModel
from app.schemas import notesCreate, noteResponse 
router = APIRouter()
@router.post("/notes", response_model=noteResponse)
async def create_note(
    note: notesCreate, 
    user_id: int = Depends(current_user), 
    db: Session = Depends(get_db)
):
    new_note = NoteModel(
        title=note.title, 
        content=note.content, 
        owner_id=user_id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
@router.get("/notes", response_model=List[noteResponse])
async def get_notes(
    user_id: int = Depends(current_user), 
    db: Session = Depends(get_db)
):
    notes = db.query(NoteModel).filter(NoteModel.owner_id == user_id).all()
    return notes
@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(
    note_id: int, 
    user_id: int = Depends(current_user), 
    db: Session = Depends(get_db)
):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    
    db.delete(note)
    db.commit()
    return None