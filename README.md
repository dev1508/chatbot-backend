# Chatbot Backend

This is a simple FastAPI application that simulates a chatbot with CRUD operations. The chatbot processes user messages, generates predefined responses, stores them in a SQLite database, and allows for editing, retrieving, and deleting messages.

## Features

- **POST**: Create a message and get a chatbot response.
- **GET**: Retrieve all messages (both user messages and chatbot responses).
- **PUT**: Edit a message, update the chatbot response, and reference the edited message.
- **DELETE**: Delete a message by ID and return a deletion status.

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- Uvicorn (ASGI server)
- SQLite (included with Python)

## Installation and Setup

Before going further please install python and pip. Follow these steps to set up and run the application locally.


### 1. Clone the repository

Run the following command to clone the repository:
```
git clone https://github.com/dev1508/chatbot-backend.git
```
Change to the cloned directory:
```
cd chatbot-backend
```
### 2. Create and activate a virtual environment

It’s recommended to use a virtual environment to manage dependencies.

For macOS and Linux:
```
python3 -m venv venv  
source venv/bin/activate
```
For Windows:
```
python -m venv venv  
venv\Scripts\activate
```
### 3. Install the required dependencies

Use pip to install all required Python packages:
```
pip install -r requirements.txt
```


### 4. Run the application

Use uvicorn to start the FastAPI server:
```
uvicorn app.main:app --reload
```
The application will now be running on `http://127.0.0.1:8000`. The `--reload` flag is useful for development as it automatically reloads the app when code changes.

### 5. Testing the Endpoints

You can use curl, Postman, or any HTTP client to interact with the API. Here are a few sample requests:

**POST** `/messages` to create a new message:
```
curl -X POST "http://127.0.0.1:8000/messages" \  
-H "Content-Type: application/json" \  
-d '{"user_message": "hello"}'
```

**GET** `/messages` to retrieve all messages:
```
curl -X GET "http://127.0.0.1:8000/messages"
```

**PUT** `/messages/{message_id}` to edit a message:

```
curl -X PUT "http://127.0.0.1:8000/messages/1" \  
-H "Content-Type: application/json" \  
-d '{"user_message": "hi"}'
```

**DELETE** `/messages/{message_id}` to delete a message:

```
curl -X DELETE "http://127.0.0.1:8000/messages/1"
```

## Project Structure

```
app/  
├── main.py  
├── database.py  
├── models.py  
├── schemas.py  
└── chatbot_responses.py
```
---

### Notes 
1. For a fresh start, you may consider deleting the existing `messages.db` file.
2. A postman collection of apis is already added in the project. You may import it.

---