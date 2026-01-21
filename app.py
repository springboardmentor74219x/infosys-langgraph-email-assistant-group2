from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any

from memory import memory
from tools import (
    hitl_edit_tool,
    send_email_tool,
    create_calendar_event_tool,
)


class AgentState(TypedDict):
    response: str
    memory: Dict[str, Any]


builder = StateGraph(AgentState)

builder.add_node("hitl", hitl_edit_tool)
builder.add_node("send_email", send_email_tool)
builder.add_node("calendar", create_calendar_event_tool)

builder.set_entry_point("hitl")
builder.add_edge("hitl", "send_email")
builder.add_edge("send_email", "calendar")
builder.add_edge("calendar", END)

app = builder.compile(checkpointer=memory)
