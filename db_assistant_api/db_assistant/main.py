"""FastAPI application exposing the /ask endpoint."""
from __future__ import annotations

import uvicorn
from fastapi import FastAPI, HTTPException

from db_assistant.llm_service import StepGenerator, QueryGenerator, AnswerGenerator
from db_assistant.models import QuestionRequest, AnswerResponse
from db_assistant.table_metadata import TABLES_MD
from db_assistant.trino_service import TrinoClient

app = FastAPI(title="DB Assistant API", version="0.1.0")


@app.post("/ask", response_model=AnswerResponse)
async def ask(req: QuestionRequest) -> AnswerResponse:  # noqa: D401
    """Answer a user's question by querying Iceberg through Trino and LLMs."""
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty")

    # 1. Generate step-by-step instructions
    steps = StepGenerator.generate(question=question, tables_metadata=TABLES_MD)

    # 2. Generate Trino query
    trino_query = QueryGenerator.generate(instructions=steps)

    # 3. Execute query
    trino_client = TrinoClient()
    try:
        data = trino_client.fetch_all(trino_query)
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=500, detail=f"Query execution failed: {exc}") from exc

    # 4. Generate answer
    answer = AnswerGenerator.generate(question=question, data_json=data)

    return AnswerResponse(answer=answer, trino_query=trino_query, steps=steps, data=data)


if __name__ == "__main__":
    uvicorn.run("db_assistant.main:app", host="0.0.0.0", port=8000, reload=True)
