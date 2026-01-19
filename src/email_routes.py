from src.classifier import generate_email

def react_agent(state):
    """
    LangGraph react node.
    Calls the email generation logic.
    """
    return generate_email(state)