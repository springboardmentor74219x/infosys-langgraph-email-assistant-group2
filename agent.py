import base64
import os.path
import re
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from langgraph.graph import StateGraph
from memory import load_memory, update_memory

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar"
]

# ----------------------------------------------------
# AUTHENTICATION
# ----------------------------------------------------

def get_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


# ----------------------------------------------------
# FETCH EMAIL (MOST RECENT UNREAD)
# ----------------------------------------------------

def fetch_unread_email():
    service = get_service()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        q="is:unread",
        maxResults=5   # fetch few to ensure latest
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return None

    # Pick MOST RECENT unread message
    msg = service.users().messages().get(
        userId="me",
        id=messages[0]["id"],
        format="full"
    ).execute()

    headers = msg["payload"]["headers"]

    subject = next(
        header["value"] for header in headers if header["name"] == "Subject"
    )

    sender = next(
        header["value"] for header in headers if header["name"] == "From"
    )

    body = ""

    if "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            if part["mimeType"] == "text/plain":
                body = base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8")
                break
    else:
        body = base64.urlsafe_b64decode(
            msg["payload"]["body"]["data"]
        ).decode("utf-8")

    return {
        "id": msg["id"],
        "threadId": msg["threadId"],
        "sender": sender,
        "subject": subject,
        "body": body
    }


# ----------------------------------------------------
# SEND REPLY
# ----------------------------------------------------

def send_reply(thread_id, to, subject, message_text):
    service = get_service()

    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    body = {
        "raw": raw,
        "threadId": thread_id
    }

    service.users().messages().send(
        userId="me",
        body=body
    ).execute()


# ----------------------------------------------------
# MOVE EMAIL TO SPAM (OPTIONAL)
# ----------------------------------------------------

def move_to_spam(message_id):
    service = get_service()

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "removeLabelIds": ["INBOX"],
            "addLabelIds": ["SPAM"]
        }
    ).execute()


# ----------------------------------------------------
# REASONING NODE (SMART NAME DETECTION)
# ----------------------------------------------------

def reasoning_node(state):

    memory = load_memory()

    email_text = state.get("email", "")
    sender_raw = state.get("sender", "")

    owner = memory.get("owner_name", "Bob")

    # Extract clean sender name
    if "<" in sender_raw:
        sender_name = sender_raw.split("<")[0].strip()
    else:
        sender_name = sender_raw

    print("DEBUG → Email Text:", email_text)

    # ------------------------------------------------
    # SMART NAME CORRECTION DETECTION
    # ------------------------------------------------

    match = re.search(r"call me (\w+)", email_text.lower())

    if match:
        new_name = match.group(1).capitalize()

        print("DEBUG → New Name Detected:", new_name)

        update_memory("name_preference", new_name)
        memory = load_memory()

        state["draft"] = f"Correction noted. I will use {new_name} going forward."
        state["memory"] = memory
        return state

    # ------------------------------------------------
    # NORMAL RESPONSE
    # ------------------------------------------------

    preferred_name = memory.get("name_preference", sender_name)

    reply = f"""Dear {preferred_name},

Thank you for your email.
I confirm the meeting as proposed.

Best regards,
{owner}
"""

    state["draft"] = reply
    state["memory"] = memory

    return state


# ----------------------------------------------------
# LANGGRAPH SETUP
# ----------------------------------------------------

graph = StateGraph(dict)

graph.add_node("reason", reasoning_node)

graph.set_entry_point("reason")

agent = graph.compile()