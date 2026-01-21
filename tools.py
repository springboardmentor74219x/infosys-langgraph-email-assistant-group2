import os
import base64
from email.message import EmailMessage

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar.events",
]


# ---------------------------
# GOOGLE AUTH
# ---------------------------
def get_creds():
    creds = None
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
    CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return creds


# ---------------------------
# HITL TOOL
# ---------------------------
def hitl_edit_tool(state):
    memory = dict(state.get("memory", {}))

    if "human_edit" in memory:
        memory["name_preference"] = memory["human_edit"]

    name = memory.get("name_preference", "Bob")
    response = f"Hi {name}, please join the meeting."

    return {**state, "response": response, "memory": memory}


# ---------------------------
# SEND EMAIL TOOL
# ---------------------------
def send_email_tool(state):
    memory = dict(state.get("memory", {}))

    if not memory.get("send_email", False):
        return {**state, "memory": memory}

    response = state.get("response", "")

    creds = get_creds()
    service = build("gmail", "v1", credentials=creds)

    message = EmailMessage()
    message.set_content(response)
    message["To"] = memory.get("to")
    message["Subject"] = "Automated Email"

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": encoded_message}
    ).execute()

    return {**state, "memory": memory}


# ---------------------------
# CALENDAR TOOL
# ---------------------------
def create_calendar_event_tool(state):
    memory = dict(state.get("memory", {}))

    if "start_time" not in memory or "end_time" not in memory:
        return {**state, "memory": memory}

    creds = get_creds()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": "Client Meeting",
        "start": {
            "dateTime": memory["start_time"],
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": memory["end_time"],
            "timeZone": "Asia/Kolkata",
        },
    }

    service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return {**state, "memory": memory}
