from sqlalchemy import Column, Integer, String, DateTime, Boolean
from rpgdiscordhelper.models.Base import Base


class UserWithoutCharacter(Base):
    __tablename__ = 'users_without_characters'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    sended_date = Column(DateTime(), nullable=False)
    server_id = Column(String(32), nullable=False)
    status = Column(Boolean(), nullable=False)
