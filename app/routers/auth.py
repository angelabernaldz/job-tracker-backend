import os
import jwt
from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from db.models import User
from db.session import get_db
from core.security import hash_password, verify_password
from utils.user import save_user_to_db
from core.security import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth")

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user: UserCreate, 
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Email already registered'
        )
    
    created_user = save_user_to_db(user, db)

    return {"Message": "User created successfully",
            "user": {
                "id": created_user.id,
                "email": created_user.email,
                "created_at": created_user.created_at
            }
    }
    

@router.post("/login")
def login(
    user: UserCreate, 
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = jwt.encode({"userId": str(db_user.id)},
                       key=SECRET_KEY,
                       algorithm=ALGORITHM)
    
    return {"Message": "User logged in successfully",
            "access_token": token,
            "token_type": "bearer"}




