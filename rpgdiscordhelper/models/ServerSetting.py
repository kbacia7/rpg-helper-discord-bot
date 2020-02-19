from sqlalchemy import Column, Integer, String, Text
from rpgdiscordhelper.models.Base import Base


class ServerSetting(Base):
    __tablename__ = 'servers_settings'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    value = Column(Text(), nullable=False)
    server_id = Column(String(32), nullable=False)
