from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal

class RouteQuery(BaseModel):
    """
    Route a user query to the most relevant datasource
    """
    datasource : Literal["vectorstore","websearch"] = Field(
        ...,
        description = "Given a user question choose to route it to web search or a vectorstore" 
    )

llm = ChatOpenAI(temperature=0)

structed_llm_router = llm.with_structured_output(RouteQuery)

system_prompt = """
you are a expert at routing a user question to a vectorstore or web search/
The vectorstore contains documents related to agents, prompt engineering and adversarial attacks on llms/
Use the vectorstore for question on these topics/
For all else, use web-search/
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , system_prompt),
        ("human" , "{question}" )
    ]
)

question_route = route_prompt | structed_llm_router

