from database import Base
from sqlalchemy import Column, Integer, String

class Passwords(Base):
    __tablename__ = 'passwords'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    website = Column(String)
    password = Column(String) 
    note = Column(String) 