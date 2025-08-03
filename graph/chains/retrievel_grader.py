from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
from graph.chains.ingestion import retriver


load_dotenv()


llm = ChatOpenAI(temperature=0)

class gradeDocument(BaseModel):
    """
    Binary score for relevance check on retrieved document
    """
    binary_score : str = Field(
        description= "Documents are relevant to the question, 'yes' or 'no' "
    )

structured_llm_grader = llm.with_structured_output(gradeDocument)

system_prompt = """
You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
If the document contains keyword or semantic meaning related to question , grade it as relevant
Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts.
"""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human","Retrieved Documents: {documents} User Question: {question}")
    ]
)

retriaval_grader = grade_prompt | structured_llm_grader

"""
if __name__ == "__main__":
    user_question = "what is the prompt engineering"
    docs = retriver.get_relevant_documents(user_question)
    retrived_document = docs[0].page_content
    print(retriaval_grader.invoke(
        {"question" : user_question,"documents" : retrived_document}
    ))
"""