"""Abstraction layer for interacting with the three LLMs.
Replace `openai.chat.completions.create` with the provider of
choice for each model.
"""
from __future__ import annotations

import os
from typing import List

from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=_OPENAI_API_KEY)


class StepGenerator(BaseModel):
    """LLM #1 – produce detailed instructions."""

    system_prompt: str = (
        "You are an expert data engineer. Generate crystal-clear, step-by-step "
        "instructions for retrieving the requested data from the available "
        "tables. Only reference columns that actually exist."
    )

    @classmethod
    def generate(cls, question: str, tables_metadata: str) -> str:
        messages = [
            {"role": "system", "content": cls.system_prompt},
            {
                "role": "user",
                "content": f"User question: {question}\n\nTables:\n{tables_metadata}",
            },
        ]
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        return response.choices[0].message.content.strip()


class QueryGenerator(BaseModel):
    """LLM #2 – translate instructions into a Trino SQL query."""

    system_prompt: str = (
        "You are a SQL expert specialised in Trino and Apache Iceberg. "
        "Generate a valid Trino query that follows the given instructions. "
        "Do not include any explanation – output *only* the SQL."
    )

    @classmethod
    def generate(cls, instructions: str) -> str:
        messages = [
            {"role": "system", "content": cls.system_prompt},
            {"role": "user", "content": instructions},
        ]
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        return response.choices[0].message.content.strip()


class AnswerGenerator(BaseModel):
    """LLM #3 – craft human-friendly answer based on data."""

    system_prompt: str = (
        "You are an insightful analyst. Using the query result in JSON form and "
        "the user's original question, write an accurate, concise response."
    )

    @classmethod
    def generate(cls, question: str, data_json: List[dict]) -> str:
        messages = [
            {"role": "system", "content": cls.system_prompt},
            {"role": "user", "content": f"Question: {question}\nData: {data_json}"},
        ]
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        return response.choices[0].message.content.strip()
