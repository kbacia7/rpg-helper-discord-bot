from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from rpgdiscordhelper.models.Base import Base
class InactiveUser(Base):
    __tablename__ = 'inactive_users'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    sended_date = Column(DateTime(), nullable=False)
    server_id = Column(String(32), nullable=False)
    status = Column(Boolean(), nullable=False)