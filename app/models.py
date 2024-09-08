from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    chat_response = Column(String, nullable=False)
    is_edited = Column(Boolean, default=False)
    edited_message_id = Column(Integer, ForeignKey('messages.id'), nullable=True)

    edited_message = relationship("Message", remote_side=[id])