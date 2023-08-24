from pydantic import BaseModel, Field, EmailStr
from schemas.company import Company
from schemas.rig import RigBasic

class User(BaseModel):
    username: str = Field(..., min_length=5)
    password:str = Field(..., min_length=5)
    email:str = EmailStr(...)
    company_id: int = Field(..., example="1")

class UserLogin(BaseModel):
    username: str = Field(..., min_length=5,example="camilo")
    password:str = Field(..., min_length=5, example="12345")
    company_id: int = Field(..., example="1")

class UserSingUp(BaseModel):
    username: str = Field(..., min_length=5)
    email:str = EmailStr(...)
    company_id: int = Field(...)

class UserBasic(BaseModel):
    username: str = Field(..., min_length=5)
    password:str = Field(..., min_length=5)
    email:str = EmailStr(...)

class UserComplete(BaseModel):
    user: UserBasic
    company: Company
    rig: RigBasic
    
