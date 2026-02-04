from sqlalchemy.orm import Session
from db.models import User
from schemas.user import UserCreate
from core.security import hash_password

def save_user_to_db(user: UserCreate, db: Session):

    db_user = User(
        email = user.email,
        password = hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user