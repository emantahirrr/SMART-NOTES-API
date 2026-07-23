from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import current_user
from app.db import get_db
from app.models import Note as NoteModel
from app.ai import call_llm
from app.schemas import summarizeIn, summarizeOut

router = APIRouter()

@router.post("/summarize", response_model=summarizeOut)
async def get_summary(
    data: summarizeIn, 
    user: str = Depends(current_user), 
    db: Session = Depends(get_db)
):
    note = db.query(NoteModel).filter(NoteModel.id == data.notes_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Summarize this note: {note.content}"}
    ]
    summary = await call_llm(messages)
    return {"summary": summary}
