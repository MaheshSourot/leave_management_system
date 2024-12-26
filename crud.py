from sqlalchemy.orm import Session
import models, schemas

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(name=user.name, email=user.email, role=user.role, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_leave(db: Session, leave: schemas.LeaveCreate, user_id: int):
    db_leave = models.Leave(user_id=user_id, **leave.dict(), status="Pending")
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave
