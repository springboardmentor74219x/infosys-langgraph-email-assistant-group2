from langgraph.graph import StateGraph
from memory import memory
from tools import send_email, create_calendar_invite

def agent_node(state):
    email = state["email"]

    if "meeting" in email.lower():
        return {
            "action": "create_calendar_invite",
            "response": "I can create a calendar invite for this meeting.",
            "paused": True
        }

    return {
        "action": "send_email",
        "response": "Drafted a professional reply email.",
        "paused": False
    }


def human_edit(state):
    # Human edits are stored in memory automatically
    state["paused"] = False
    return state


graph = StateGraph(dict)
graph.add_node("agent", agent_node)
graph.add_node("human", human_edit)

graph.set_entry_point("agent")
graph.add_edge("agent", "human")

app = graph.compile(checkpointer=memory)