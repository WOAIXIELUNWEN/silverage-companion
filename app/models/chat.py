import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.models.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), index=True, nullable=False)
    role = Column(String(16), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    intent = Column(String(32), default="chat")  # chat / health / emergency
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
