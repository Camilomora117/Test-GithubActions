from pydantic import BaseModel, Field, EmailStr

class Rig(BaseModel):
    name: str = Field(..., min_length=5)
    company_id: int = Field(..., example="1")
    user_id: int = Field(..., example="1")

class RigBasic(BaseModel):
    name: str = Field(..., min_length=5)