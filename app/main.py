from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from .chatbot_responses import chatbot_responses

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.post("/messages", response_model=schemas.MessageResponse)
def create_message(message: schemas.MessageCreate, db: Session = Depends(database.get_db)):

    response = chatbot_responses.get(message.user_message.lower(), "I'm not sure how to respond to that.")

    db_message = models.Message(user_message=message.user_message, chat_response=response)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@app.get("/messages", response_model=List[schemas.MessageResponse])
def get_all_messages(db: Session = Depends(database.get_db)):
    return db.query(models.Message).all()


@app.put("/messages/{message_id}", response_model=schemas.MessageResponse)
def edit_message(message_id: int, updated_message: schemas.MessageUpdate, db: Session = Depends(database.get_db)):

    original_message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not original_message:
        raise HTTPException(status_code=404, detail="Message not found")

    response = chatbot_responses.get(updated_message.user_message.lower(), "I'm not sure how to respond to that.")

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
    return new_message


@app.delete("/messages/{message_id}", response_model=schemas.MessageResponse)
def delete_message(message_id: int, db: Session = Depends(database.get_db)):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    db.delete(message)
    db.commit()
    return message