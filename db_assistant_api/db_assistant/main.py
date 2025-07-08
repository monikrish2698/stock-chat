from fastapi import FastAPI
from dotenv import load_dotenv
from routes.chat_router import chat_router

from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # or ["http://localhost:8501"]
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/hello")
def test_connection():
    return "Hello, I am your trading educator!"
