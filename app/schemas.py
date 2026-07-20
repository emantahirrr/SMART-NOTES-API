from pydantic import BaseModel, EmailStr, Field
from typing import Optional
class userCreate(BaseModel):
    username: str=Field(...,min_length=3,max_length=30)
    password: str=Field(...,min_length=8)
class userPublic(BaseModel):
    id: str
    username: str
class notesCreate(BaseModel):
    title: str=Field(...,min_length=3,max_length=30)
    content: str=Field(...,min_length=1)
class notesPublic(BaseModel):
    id: str
    title: str
    content: str
    owner_id:int
class noteResponse(BaseModel):
    id: int
    content: str
    owner_id: int
    class Config:
        from_attributes = True
class summarizeIn(BaseModel):
    notes_id: int
class summarizeOut(BaseModel):
    summary: str