from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
from services.llm_service import LLMService
from models.chat_model import ChatRequest
from typing import Dict
from common_helper import event_generator
from database.trinoQueryEngine import TrinoQueryEngine

chat_router = APIRouter()

@chat_router.post("/chat")
async def chat(request: ChatRequest):
    question = request.question
    ticker = request.ticker
    from_date = request.from_date
    to_date = request.to_date

    llm_service = LLMService()
    """
    get the intent of the question
    """
    question += "\nticker chosen by the user: " + ticker
    if from_date is not None:
        question += "\nfrom date: " + from_date.strftime("%Y-%m-%d")
    if to_date is not None:
        question += "\nto date: " + to_date.strftime("%Y-%m-%d")
    intent = llm_service.get_intent(question)
    print(intent)
    """
    generate steps based on the intent
    """
    steps = llm_service.generate_steps(question, intent)
    print(steps)
    """
    generate trino query based on the steps
    """
    query = llm_service.generate_trino_query(steps)
    print(query['query'])
    """
    execute the query
    """
    query_string = query['query']
    data = llm_service.trino_instance.execute_query(query_string)
    print(data)
    """
    generate summary based on the data
    """
    return StreamingResponse(
        event_generator(llm_service.generate_summary(data, intent, question)),
        media_type="text/event-stream"    
    )
    
