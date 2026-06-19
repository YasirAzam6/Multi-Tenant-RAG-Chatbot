import os
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from graph.state.graph_state import RAGState
from graph.nodes.query_node import query_node
from graph.nodes.retrival_node import retrieval_node
from graph.nodes.re_rank_node import rerank_node
from graph.nodes.prompt_node import prompt_node
from graph.nodes.llm_node import llm_node
from graph.nodes.router_node import router_node
from graph.nodes.direct_llm_node import direct_llm_node


def build_graph():
    graph = StateGraph(RAGState)

    graph.add_node("query", query_node)
    graph.add_node("router", router_node)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("rerank", rerank_node)
    graph.add_node("prompt", prompt_node)
    graph.add_node("llm", llm_node)
    graph.add_node("direct_llm", direct_llm_node)

    graph.add_edge(START, "query")
    graph.add_edge("query", "retrieval")
    graph.add_edge("retrieval", "rerank")
    graph.add_edge("rerank", "prompt")
    graph.add_edge("prompt", "llm")
    graph.add_edge("llm", END)

    # On Vercel: skip MemorySaver — it causes Errno 16 from lock file contention
    if os.environ.get("VERCEL") == "1":
        return graph.compile()  # stateless
    
    memory_saver = MemorySaver()
    return graph.compile(checkpointer=memory_saver)