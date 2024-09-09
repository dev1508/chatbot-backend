from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from .chatbot_responses import chatbot_responses
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

@app.post("/messages", response_model=schemas.ChatResponse)
def create_message(message: schemas.MessageCreate, db: Session = Depends(database.get_db)):

    response = find_chatbot_response(message.user_message)

    db_message = models.Message(user_message=message.user_message, chat_response=response)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return {"chat_response": response, "id": db_message.id}


@app.get("/messages", response_model=List[schemas.MessageResponse])
def get_all_messages(db: Session = Depends(database.get_db)):
    return db.query(models.Message).all()


@app.put("/messages/{message_id}", response_model=schemas.ChatResponse)
def edit_message(message_id: int, updated_message: schemas.MessageUpdate, db: Session = Depends(database.get_db)):

    original_message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not original_message:
        raise HTTPException(status_code=404, detail="Message not found")

    if original_message.is_edited:
        raise HTTPException(status_code=400, detail="Already edited")

    response = find_chatbot_response(updated_message.user_message)

    original_message.is_edited = True
    db.commit()

    new_message = models.Message(
        user_message=updated_message.user_message,
        chat_response=response,
        edited_message_id=original_message.id
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return {"chat_response": response, "id": new_message.id}


@app.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(database.get_db)):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    db.delete(message)
    db.commit()

    return {"status": "Message deleted successfully"}


def find_chatbot_response(user_message: str) -> str:

    user_message = user_message.lower()

    for key in chatbot_responses:
        if key in user_message:
            return chatbot_responses[key]

    return "I'm not sure how to respond to that."