from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key= True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))

