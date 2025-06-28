from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., example="What were the total sales by region last quarter?")


class AnswerResponse(BaseModel):
    answer: str
    trino_query: str
    steps: str
    data: List[dict]
