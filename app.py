from langgraph.graph import StateGraph, END
from tools import (
    hitl_edit_tool,
    send_email_tool,
    create_calendar_event_tool,
)

# Use dynamic state
AgentState = dict

builder = StateGraph(AgentState)

builder.add_node("hitl", hitl_edit_tool)
builder.add_node("send_email", send_email_tool)
builder.add_node("calendar", create_calendar_event_tool)

builder.set_entry_point("hitl")
builder.add_edge("hitl", "send_email")
builder.add_edge("send_email", "calendar")
builder.add_edge("calendar", END)

# ❌ REMOVE checkpointer
app = builder.compile()
