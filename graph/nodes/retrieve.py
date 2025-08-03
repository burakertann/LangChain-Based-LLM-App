from graph.chains import ingestion
from graph.state import GraphState
from typing import Dict, Any
from graph.chains.ingestion import retriver

def retrieve(state : GraphState) -> Dict[str,Any]:
    print("------ Retrieve -------")
    
    question = state["question"]
    documents = retriver.invoke(question)

    return {"question" : question, "documents" : documents}