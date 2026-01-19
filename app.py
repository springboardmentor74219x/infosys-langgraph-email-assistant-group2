from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

# 1. Define tools locally to fix the ImportError
def send_email(email_content: str):
    return f"Action: Email sent with content: {email_content}"

def create_calendar_invite(details: str):
    return f"Action: Calendar invite created for: {details}"

# 2. Define the State structure
class AgentState(TypedDict):
    email: str
    action: str
    response: str

# 3. Define the Agent Node using the 2026 Interrupt pattern
def agent_node(state: AgentState):
    email = state["email"]

    if "meeting" in email.lower():
        # Execution pauses here. The string is the prompt for the human.
        # This replaces the manual 'paused' flag.
        human_review = interrupt("I can create a calendar invite for this meeting. Please approve.")
        
        return {
            "action": "create_calendar_invite",
            "response": f"I can create a calendar invite for this meeting. (Human said: {human_review})"
        }

    return {
        "action": "send_email",
        "response": "Drafted a professional reply email."
    }

# 4. Build the Graph
# We no longer need a separate 'human' node as 'interrupt' handles the pause.
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)

graph.add_edge(START, "agent")
graph.add_edge("agent", END)

# 5. Compile with Checkpointer (Required for interrupts)
memory = MemorySaver()
app = workflow = graph.compile(checkpointer=memory)
