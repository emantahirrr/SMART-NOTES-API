from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth import make_token, hash_pw, verify_password 
from app.db import get_db
from app.models import User as UserModel 
from app.schemas import userCreate
router = APIRouter()
@router.post("/register")
async def register_user(user: userCreate, db: Session = Depends(get_db)):
    hashed_password = hash_pw(user.password)
    if hashed_password is None:
        raise HTTPException(status_code=500, detail="Password hashing failed")
    new_user = UserModel(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}
@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = make_token(user.id)
    return {"access_token": token, "token_type": "bearer"}