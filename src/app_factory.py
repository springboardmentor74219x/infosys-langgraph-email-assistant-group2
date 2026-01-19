from langgraph.graph import StateGraph

from src.classifier import triage_node
from src.email_routes import react_agent


def build_app():
    graph = StateGraph(dict)

    graph.add_node("triage", triage_node)
    graph.add_node("react", react_agent)

    def route(state):
        if state["triage"] == "respond":
            return "react"
        return "end"

    graph.add_conditional_edges("triage", route)
    graph.set_entry_point("triage")

    return graph.compile()