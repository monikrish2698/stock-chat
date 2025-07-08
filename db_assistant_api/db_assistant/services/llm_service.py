import os
import json
import asyncio
import token
from typing import AsyncIterable
from datetime import datetime, timezone
import ast

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, prompt
from langchain.chat_models import init_chat_model
from database.trinoQueryEngine import TrinoQueryEngine
from models.query_model import QueryOutput
from langchain_core.output_parsers import StrOutputParser

from prompts.prompts import Prompt

class LLMService:
    def __init__(self):
        self.trino_instance = TrinoQueryEngine()
        self.prompt_instance = Prompt()
        self.metadata = self.prompt_instance.get_metadata()
        self.reference_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    def get_intent(self, question: str):
        intent_llm = ChatOpenAI(model_name="o4-mini", temperature = 1, verbose = True)
        intent_prompt = self.prompt_instance.get_intent_prompt()
        intent_prompt_template = PromptTemplate(template=intent_prompt, input_variables=["question", "reference_date"])
        intent_llm_chain = intent_prompt_template | intent_llm | StrOutputParser()
        response = intent_llm_chain.invoke({"question":question, "reference_date":self.reference_date})
        return response

    def generate_steps(self, question: str, intent_summary: str):
        analyst_llm = ChatOpenAI(model_name="o4-mini", temperature = 1, verbose = True)
        analyst_prompt = self.prompt_instance.get_data_retrieval_planner_prompt()
        analyst_prompt_template = PromptTemplate(template = analyst_prompt, input_variables = ["question", "intent_summary", "metadata"])
        analyst_llm_chain = analyst_prompt_template | analyst_llm | StrOutputParser()
        response = analyst_llm_chain.invoke({"question":question, "intent_summary":intent_summary, "metadata":self.metadata})
        return response
    
    def generate_trino_query(self, steps:str):
        trino_query_llm = ChatOpenAI(model_name="o4-mini", temperature = 1, verbose = True)
        structured_trino_query_llm = trino_query_llm.with_structured_output(QueryOutput)
        trino_query_prompt = self.prompt_instance.get_data_analyst_prompt()
        query_template = ChatPromptTemplate([("system", trino_query_prompt)])

        prompt = query_template.invoke({
            "detailed_instructions": steps,
            "metadata": self.metadata
        })
        result = structured_trino_query_llm.invoke(prompt)
        return {"query": result["query"]}

    async def generate_summary(
        self, 
        data, 
        intent_summary: str, 
        question: str
    ) -> AsyncIterable[str]:
        asyncCallback = AsyncIteratorCallbackHandler()
        try:
            summarise_data_llm = ChatOpenAI(
                                model_name="o4-mini", 
                                temperature = 1, 
                                verbose = True,
                                callbacks=[asyncCallback],
                                streaming=True
                            )
            summarise_data_prompt = self.prompt_instance.get_summarise_data_prompt()
            summary_prompt_template = PromptTemplate(
                template = summarise_data_prompt, 
                input_variables = ["data", "intent_summary", "question"]
            )
            
            summary_llm_chain = summary_prompt_template | summarise_data_llm | StrOutputParser()
            response = asyncio.create_task(
                summary_llm_chain.ainvoke({"data":data, "intent_summary":intent_summary, "question":question})
            )
            streamedChunks = ""
            try:
                async for token in asyncCallback.aiter():
                    streamedChunks += token

                    yield json.dumps(
                        {"parts": token, "status": "in-progress", "type" : "chat"}
                    )
            except Exception as e:
                yield {
                    "type" : "chat",
                    "status" : "error",
                    "parts" : "An error occurred while generating the summary"
                }
            finally:
                yield json.dumps(
                    {
                        "parts" : "",
                        "status" : "done",
                        "type" : "chat"
                    }
                )
            await response
        except Exception as e:
            yield {
                "type" : "chat",
                "status" : "error",
                "parts" : "An error occurred while generating the summary"
            }
            raise Exception
        
    
# service_check = LLMService()
# trino_engine = TrinoQueryEngine()

# question = """
# Can you tell me the how to find if a stock is in a downward trend?
# ticker chosen by the user: AAPL
# """
# intent = service_check.get_intent(question)
# print(intent, "\n")
# steps = service_check.generate_steps(question, intent)
# print(steps, "\n")
# query = service_check.generate_trino_query(steps)
# query_string = query['query']
# print(query_string)
# data = trino_engine.execute_query(query_string)
# print(data)
# summary = service_check.generate_summary(data, intent, question)
# print(summary)
