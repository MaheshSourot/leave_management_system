from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    name: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class LeaveBase(BaseModel):
    start_date: date
    end_date: date
    leave_type: str

class LeaveCreate(LeaveBase):
    pass

class Leave(LeaveBase):
    id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True

class ArroveLeave(BaseModel):
    email:str
    status:str
    start_date:str

class Token(BaseModel):
    email:str
    password:str 

