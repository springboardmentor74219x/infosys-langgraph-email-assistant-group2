# from langgraph.graph import StateGraph

# # -----------------------------
# # Human-in-the-loop node
# # -----------------------------
# def human_edit(state):
#     text = state.get("input", "").lower()
#     memory = state.get("memory", {})

#     if "call him robert" in text:
#         memory["name_preference"] = "Robert"

#     state["memory"] = memory
#     return state


# # -----------------------------
# # Agent node
# # -----------------------------
# def agent_node(state):
#     user_input = state.get("input", "")
#     memory = state.get("memory", {})

#     name = memory.get("name_preference", "Bob")

#     if "meeting" in user_input.lower():
#         response = f"""Dear {name},

# I hope you are doing well.
# This is a reminder about our meeting scheduled for tomorrow.

# Best regards,
# """
#     else:
#         response = f"""Dear {name},

# This is a professional email.

# Best regards,
# """

#     return {
#         "response": response,
#         "memory": memory,
#         "paused": False
#     }


# # -----------------------------
# # Build graph
# # -----------------------------
# graph = StateGraph(dict)

# graph.add_node("human", human_edit)
# graph.add_node("agent", agent_node)

# # ✅ HUMAN FIRST
# graph.set_entry_point("human")
# graph.add_edge("human", "agent")

# # -----------------------------
# # Compile
# # -----------------------------
# app = graph.compile()





# from langgraph.graph import StateGraph
# from tools import send_email_node

# # -----------------------------
# # HUMAN-IN-THE-LOOP NODE
# # -----------------------------
# def human_edit(state):
#     text = state.get("input", "").lower()
#     memory = state.get("memory", {})

#     if "call him robert" in text:
#         memory["name_preference"] = "Robert"

#     state["memory"] = memory
#     return state

# # -----------------------------
# # AGENT NODE
# # -----------------------------
# def agent_node(state):
#     memory = state.get("memory", {})
#     name = memory.get("name_preference", "Bob")

#     subject = "Meeting Reminder"
#     body = f"""Dear {name},

# I hope you are doing well.
# This is a reminder about our meeting scheduled for tomorrow.

# Best regards,
# Assistant"""

#     # FIX: Return complete state dict with ALL keys
#     return {
#         **state,  # Preserve existing state
#         "to": "naaz83651@gmail.com",
#         "subject": subject,
#         "body": body,
#         "response": body,
#         "memory": memory
#     }

# # -----------------------------
# # SEND EMAIL NODE WRAPPER
# # -----------------------------
# def send_email_node_wrapper(state):
#     return send_email_node(state)

# # -----------------------------
# # BUILD GRAPH
# # -----------------------------
# graph = StateGraph(dict)

# graph.add_node("human", human_edit)
# graph.add_node("agent", agent_node)
# graph.add_node("send_email", send_email_node_wrapper)

# graph.set_entry_point("human")

# # Flow: human -> agent -> send_email
# graph.add_edge("human", "agent")
# graph.add_edge("agent", "send_email")

# # -----------------------------
# # COMPILE APP
# # -----------------------------
# app = graph.compile()
# print("App compiled successfully!")



# app.py  
from langgraph.graph import StateGraph, END
from tools import send_email_node

def human_edit(state):
    text = state.get("input", "").lower()
    memory = state.get("memory", {})
    if "call him robert" in text:
        memory["name_preference"] = "Robert"
    return {**state, "memory": memory}

def agent_node(state):
    memory = state.get("memory", {})
    name = memory.get("name_preference", "Bob")
    subject = "Meeting Reminder"
    body = f"""Dear {name},

I hope you are doing well.
This is a reminder about our meeting scheduled for tomorrow.

Best regards,
Assistant"""
    return {
        "input": state.get("input", ""),
        "memory": memory,
        "to": "naaz83651@gmail.com",
        "subject": subject,
        "body": body,
        "response": body
    }

def send_email_node_wrapper(state):
    return send_email_node(state)

graph = StateGraph(dict)
graph.add_node("human", human_edit)
graph.add_node("agent", agent_node)
graph.add_node("send_email", send_email_node_wrapper)

graph.set_entry_point("human")
graph.add_edge("human", "agent")
graph.add_edge("agent", "send_email")
graph.add_edge("send_email", END)

app = graph.compile()
print("✅ App compiled successfully!")
