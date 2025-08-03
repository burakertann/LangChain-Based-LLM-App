from graph.node_constants import RETRIEVE,GRADE_DOCUMENTS,GENERATE,WEBSEARCH
from graph.nodes.retrieve import retrieve
from graph.nodes.generate import generate
from graph.nodes.grade_documents import grade_documents
from graph.nodes.web_search import web_search
from graph.chains.router import question_route,RouteQuery
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.answer_grader import  answer_grader
from langgraph.graph import END,StateGraph
from dotenv import load_dotenv

load_dotenv()

def decide_to_generate(state : GraphState):
    print("----ASSES GRADED DOCUMENT----")
    if state["web_search"]:
        print("---WEB SEARCH----")
        return WEBSEARCH
    else:
        return GENERATE

def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"

def route_question(state: GraphState) -> str:
    print("---ROUTE QUESTION---")
    question = state["question"]
    source: RouteQuery = question_route.invoke({"question": question})
    if source.datasource == WEBSEARCH:
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE



workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE,retrieve)
workflow.add_node(GENERATE,generate)
workflow.add_node(WEBSEARCH,web_search)
workflow.add_node(GRADE_DOCUMENTS,grade_documents)

workflow.set_conditional_entry_point(
    route_question,
    path_map={
        WEBSEARCH : WEBSEARCH,
        RETRIEVE : RETRIEVE
    }
)
    
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)

workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    path_map={
        WEBSEARCH : WEBSEARCH,
        GENERATE : GENERATE
    }
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    path_map= {
        "not supported" : GENERATE,
        "useful" : END,
        "not useful": WEBSEARCH
    }
)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)


app = workflow.compile()


