from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime
import schemas, database, models
from database import SessionLocal
from schemas import LeaveCreate,Leave
from routers.auth import get_current_user

router = APIRouter()

user_dependency=Annotated[dict,Depends(get_current_user)]
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]



@router.post("/", response_model=Leave)
def create_leave(
    leave: LeaveCreate, 
    db: db_dependency,
    current_user:user_dependency
):
    if leave.end_date < leave.start_date:
        raise HTTPException(status_code=400, detail="End date cannot be before start date")
    leave_data = models.Leaves(
        user_id=current_user.id,
        start_date=leave.start_date,
        end_date=leave.end_date,
        leave_type=leave.leave_type,
        status="Pending"
    )
    db.add(leave_data)
    db.commit()
    db.refresh(leave_data)
    return leave_data

@router.get("/", response_model=list[schemas.Leave])
def get_user_leaves(
    db: db_dependency, 
    current_user:user_dependency
):
    leaves = db.query(models.Leaves).filter(models.Leaves.user_id == current_user.id).all()
    if not leaves:
        raise HTTPException(status_code=404, detail="No leaves found for the current user")
    return leaves

@router.put("/approve_leave")
def update_leave_status(
    update_leave:schemas.ArroveLeave,
    db: db_dependency,
    current_user: user_dependency,
    
    
):
    if current_user.role in ['HR', 'RM']:
        user=db.query(models.Users).filter(models.Users.email==update_leave.email).first()
       
        leave = db.query(models.Leaves).filter(
            models.Leaves.user_id == user.id,
            models.Leaves.start_date==update_leave.start_date
        )
        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")
       
        
        leave.update({"status": update_leave.status})
        db.commit()
        
        return {"message":"Successfully Updated"}