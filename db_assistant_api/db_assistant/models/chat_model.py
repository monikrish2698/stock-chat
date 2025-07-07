from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique Streamlit session ID")
    question:   str = Field(..., description="The user's question")
    ticker:     str = Field(..., description="Stock ticker symbol")
    from_date:  Optional[date] = Field(
        None,
        description="(optional) start date, will be parsed as YYYY-MM-DD"
    )
    to_date:    Optional[date] = Field(
        None,
        description="(optional) end date, will be parsed as YYYY-MM-DD"
    )

class QuerySchema(BaseModel):
    list[str]
    