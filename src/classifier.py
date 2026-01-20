from src.memory import save_memory, get_memory
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def generate_email(state):
    """
    This function is the brain of the agent.
    It reads memory, injects it into the prompt,
    and generates the email.
    """

    user = state["user"]
    email = state["email"]

    # Load memory
    memory = get_memory(user)

    # Build memory prompt
    memory_prompt = ""
    if "name" in memory:
        memory_prompt = f"User prefers the name {memory['name']}. Always use this name."

    prompt = f"""
You are a professional email assistant.

{memory_prompt}

Incoming Email:
{email}

Write a clear and professional reply.
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content,
        "memory": memory
    }


def learn_from_edit(state):
    """
    This is the HITL learning step.
    When a human edits the response, we store it in memory.
    """

    user = state["user"]
    edited_text = state["edited"]

    # If user corrected the name, store it
    if "Robert" in edited_text:
        save_memory(user, {"name": "Robert"})

    return {"status": "memory updated"}

def triage_node(state):
    """
    Decide whether the agent should respond or stop.
    This is required for the LangGraph routing step.
    """

    email = state["email"]

    # Simple triage logic (can be improved later)
    if "unsubscribe" in email.lower():
        decision = "end"
    else:
        decision = "respond"

    return {
        **state,
        "triage": decision
    }