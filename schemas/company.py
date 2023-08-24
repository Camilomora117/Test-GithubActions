from pydantic import BaseModel, Field, EmailStr

class Company(BaseModel):
    name: str = Field(..., min_length=5, example="SkanHawk")
    description:str = Field(..., min_length=5, max_length=100, example="Empresa de Analisis de Datos")
    email:str = EmailStr(...)
    phone: int = Field(..., example=32038231)