import os
import json
import asyncio
import token
from typing import AsyncIterable
from datetime import datetime, timezone

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, prompt
from langchain.chat_models import init_chat_model
from database.trinoQueryEngine import TrinoQueryEngine
from models.query_model import QueryOutput

from database.trinoQueryEngine import TrinoQueryEngine
from prompts.prompts import Prompt

class LLMService:
    def __init__(self):
        self.trino_instance = TrinoQueryEngine()
        self.prompt_instance = Prompt()
        self.metadata = self.prompt_instance.get_metadata()
        self.reference_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    def get_intent(self, question: str):
        intent_llm = ChatOpenAI(
            model_name="o4-mini", 
            temperature = 1, 
            verbose = True
        )
        intent_prompt = self.prompt_instance.get_intent_prompt()
        intent_prompt_template = PromptTemplate(template=intent_prompt, input_variables=["question", "reference_date"])
        intent_llm_chain = LLMChain(prompt=intent_prompt_template, llm=intent_llm)
        response = intent_llm_chain.invoke({"question":question, "reference_date":self.reference_date})
        return response['text']

    def generate_steps(self, question: str, intent_summary: str):
        analyst_llm = ChatOpenAI(
            model_name="o4-mini", 
            temperature = 1, 
            verbose = True
        )
        analyst_prompt = self.prompt_instance.get_analyst_prompt()
        analyst_prompt_template = PromptTemplate(template = analyst_prompt, input_variables = ["question", "intent_summary", "metadata"])
        analyst_llm_chain = LLMChain(prompt = analyst_prompt_template, llm = analyst_llm)
        response = analyst_llm_chain.invoke({"question":question, "intent_summary":intent_summary, "metadata":self.metadata})
        return response['text']
    
    def generate_trino_query(self, steps:str, question:str):
        trino_query_llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        structured_trino_query_llm = trino_query_llm.with_structured_output(QueryOutput)
        trino_query_prompt = self.prompt_instance.get_trino_query_prompt()
        user_prompt = "Question: {question}"
        query_template = ChatPromptTemplate([("system", trino_query_prompt), ("user", user_prompt)])

        prompt = query_template.invoke({
            "steps": steps,
            "metadata": self.metadata,
            "question": question
        })
        result = structured_trino_query_llm.invoke(prompt)
        return {"query": result["query"]}

    async def summarise_data(
        self, 
        data: str, 
        question: str
        ) -> AsyncIterable[str]:
        asyncCallback = AsyncIteratorCallbackHandler()
        summarise_data_llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        summarise_data_prompt = self.prompt_instance.get_summarise_data_prompt()
        user_prompt = "Question: {question}"
        query_template = ChatPromptTemplate([("system", summarise_data_prompt), ("user", user_prompt)])
        prompt = query_template.invoke({
            "question": question,
            "data": data
        })
        # response = asyncio.create_task(summarise_data_llm.ainvoke(prompt))
        streamedChunks = ""
        try:
            async for chunk in summarise_data_llm.astream(prompt):
                streamedChunks += chunk.content
                yield json.dumps(
                    {"parts" : chunk.content, "status" : "in-progress", "type" : "chat"}
                )
        except Exception as e:
            yield {
                "type" : "chat",
                "status" : "error",
                "parts" : "An error occurred while processing the request."
            }
        finally:
            yield json.dumps({
                "type" : "chat",
                "status" : "completed",
                "parts" : ""
            })
        
    
service_check = LLMService()
# trino_engine = TrinoQueryEngine()

question = """
I don't know what moving averages are. Can you help me understand what it is by showing me some example data of Apple?
"""
intent = service_check.get_intent(question)

print(intent)
steps = service_check.generate_steps(question, intent)
print(steps)
# response = service_check.generate_steps("What was the close price of AAPL on 2021-02-17?")
# query = service_check.generate_trino_query(response, "What was the close price of AAPL on 2021-02-17?")
# print(query)
# data = trino_engine.execute_query(query["query"])
# print(data)
# summarise_data = service_check.summarise_data(data, "What was the close price of AAPL on 2021-02-17?")
# print(summarise_data)

