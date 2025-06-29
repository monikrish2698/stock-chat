from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
from services.llm_service import LLMService
from models.chat_model import ChatRequest
from typing import Dict
from common_helper import event_generator
from database.trinoQueryEngine import TrinoQueryEngine

chat_router = APIRouter()

@chat_router.get("/chat")
async def chat(request: ChatRequest, http_request: Request):
    question = request.question
    llm_service = LLMService()
    trino_engine = TrinoQueryEngine()
    steps = llm_service.generate_steps(question)
    query = llm_service.generate_trino_query(steps, question)
    data = trino_engine.execute_query(query["query"])
    return StreamingResponse(event_generator(llm_service.summarise_data(data, question)), media_type="text/event-stream")
