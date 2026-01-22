from langgraph.graph import StateGraph

# -----------------------------
# Human-in-the-loop node
# -----------------------------
def human_edit(state):
    text = state.get("input", "").lower()
    memory = state.get("memory", {})

    if "call him robert" in text:
        memory["name_preference"] = "Robert"

    state["memory"] = memory
    return state


# -----------------------------
# Agent node
# -----------------------------
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


# -----------------------------
# Build graph
# -----------------------------
graph = StateGraph(dict)

graph.add_node("human", human_edit)
graph.add_node("agent", agent_node)

# ✅ HUMAN FIRST
graph.set_entry_point("human")
graph.add_edge("human", "agent")

# -----------------------------
# Compile
# -----------------------------
app = graph.compile()