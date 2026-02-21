def triage(email_body):

    text = email_body.lower()

    # Spam detection
    if any(word in text for word in [
        "lottery", "prize", "winner", "click here",
        "urgent offer", "claim now"
    ]):
        return "ignore"

    # Security / alerts
    if any(word in text for word in [
        "security alert",
        "suspicious",
        "login attempt",
        "password reset",
        "verify your account"
    ]):
        return "notify"

    # Meeting / business intent
    if any(word in text for word in [
        "meeting",
        "schedule",
        "sync",
        "connect",
        "tomorrow",
        "pm",
        "am"
    ]):
        return "respond"

    # Default safety
    return "notify"