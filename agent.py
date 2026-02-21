import base64
import os.path
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar"
]

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

def fetch_unread_email():
    service = get_service()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        q="is:unread",
        maxResults=1
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return None

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

def create_calendar_event(summary, start_time, end_time):
    service = build("calendar", "v3", credentials=get_service()._http.credentials)

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Kolkata"
        }
    }

    service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

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
from langgraph.graph import StateGraph
from memory import load_memory, update_memory
def reasoning_node(state):

    from memory import load_memory, update_memory

    memory = load_memory()

    email_text = state.get("email", "").lower()
    sender_name = state.get("sender_name", "User")
    thread_id = state.get("threadId")

    owner = memory.get("owner_name", "Bob")

    # --------------------------------
    # CORRECTION CASE
    # --------------------------------
    if "call me robert" in email_text and "not suresh" in email_text:
        update_memory("name_preference", "Robert")
        memory = load_memory()

        state["draft"] = "Correction noted. I will use Robert going forward."
        state["memory"] = memory
        return state

    # --------------------------------
    # NORMAL RESPONSE FLOW
    # --------------------------------
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
    # ----------------------------
    # NORMAL RESPONSE
    # ----------------------------

    preferred_name = memory.get("name_preference", sender_name)

    reply = f"""
Dear {sender_name},

Thank you for your email.
I confirm the meeting as proposed.

Best regards,
{owner_name}
"""

    state["draft"] = reply.strip()
    return state

graph = StateGraph(dict)
graph.add_node("reason", reasoning_node)
graph.set_entry_point("reason")

agent = graph.compile()