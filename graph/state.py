from typing import TypedDict,List

class GraphState(TypedDict):
    """
    represent the state of the graph
    Attributes:
        question : question
        generation : LLM generation
        web_search : whether to add search or not
        documents : list of documents
    """
    question : str
    generation : str
    web_search : bool
    documents : List[str]