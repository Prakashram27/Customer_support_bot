from database import Base
from sqlalchemy import Column, Integer,String

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index= True)
    username = Column(String, unique = True)
    hashed_password = Column(String)