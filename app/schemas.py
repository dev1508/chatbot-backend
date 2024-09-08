from pydantic import BaseModel
from typing import Optional

class MessageBase(BaseModel):
    user_message: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(MessageBase):
    pass

class ChatResponse(BaseModel):
    chat_response: str

class MessageResponse(BaseModel):
    id: int
    user_message: str
    chat_response: str
    is_edited: bool
    edited_message_id: Optional[int] = None

    class Config:
        orm_mode = True