from src.memory import save_memory, get_memory
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

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