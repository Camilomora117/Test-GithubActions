from config.database import Base
from sqlalchemy import Column, Integer, String

class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key= True)
    name = Column(String, unique=True)
    description = Column(String)
    email = Column(String, unique=True)
    phone = Column(Integer)