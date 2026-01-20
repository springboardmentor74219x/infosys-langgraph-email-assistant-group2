from langgraph.graph import StateGraph, END
from memory import memory

def human_edit(state):
    text = state.get("input", "").lower()
    memory = state.get("memory", {})

    if "call him robert" in text:
        memory["name_preference"] = "Robert"

    state["memory"] = memory
    return state


def agent_node(state):
    user_input = state.get("input", "")
    memory = state.get("memory", {})

    name = memory.get("name_preference", "Bob")

    if "meeting" in user_input.lower():
        response = f"""Dear {name},

I hope you are doing well.
This is a reminder about our meeting scheduled for tomorrow.

Best regards,
"""
    else:
        response = f"""Dear {name},

This is a professional email.

Best regards,
"""

    return {
        "response": response,
        "memory": memory,
        "paused": False
    }


builder = StateGraph(dict)

builder.add_node("human", human_edit)
builder.add_node("agent", agent_node)


builder.set_entry_point("human")
builder.add_edge("human", "agent")
builder.add_edge("agent", END)

app = builder.compile(checkpointer=memory)