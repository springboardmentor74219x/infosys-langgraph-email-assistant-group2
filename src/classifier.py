from src.memory import get_memory, save_memory
def generate_email(state):
    user = state["user"]
    email = state["email"]

    memory = get_memory(user)

    memory_prompt = ""
    if "name" in memory:
        memory_prompt = f"User prefers the name {memory['name']}. Always use this."

    prompt = f"""
You are a professional email assistant.

{memory_prompt}

Incoming email:
{email}
"""

    return {
        "response": prompt
    }
def learn_from_edit(state, edited_text):
    user = state["user"]

    if "Robert" in edited_text:
        save_memory(user, {"name": "Robert"})

    return {"status": "memory updated"}