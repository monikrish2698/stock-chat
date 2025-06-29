from fastapi import FastAPI
from dotenv import load_dotenv
from routes.chat_router import chat_router


load_dotenv()

app = FastAPI()

@app.get("/hello")
def test_connection():
    return "Hello, I am your trading educator!"

app.include_router(chat_router)
