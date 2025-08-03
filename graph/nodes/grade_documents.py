from typing import Any,Dict
from graph.chains.retrievel_grader import retriaval_grader
from graph.state import GraphState


def grade_documents(state : GraphState) -> Dict[str,Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run a web search
    Args : 
        state (dict) : The current state of the graph 
    Returns :
        state (dict) : Filtered out irrelevant documents and updated web_search state
    """
    print("----- CHECKİNG THE DOCUMENT RELEVANT TO QUESTİON")
    
    question = state["question"]
    documents = state["documents"]
    web_search = False
    
    filtered_docs = []

    for d in documents:
        score = retriaval_grader.invoke(
            {"question" : question, "documents" : d.page_content}
        )
        grade = score.binary_score

        if grade.lower() == "yes":
            filtered_docs.append(d)
            print("----Grade document relevant----")
        else:
            print("----Grade document irrelevant----")
            web_search = True
            continue

    
    
    return {"question" : question, "documents" : filtered_docs, "web_search": web_search}