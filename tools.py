# import os
# import base64
# import pickle
# from email.message import EmailMessage

# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials

# # ------------------------
# # SCOPES
# # ------------------------
# SCOPES = [
#     "https://www.googleapis.com/auth/gmail.send",
#     "https://www.googleapis.com/auth/calendar.events",
# ]

# # ------------------------
# # AUTH HELPER
# # ------------------------
# def get_creds():
#     creds = None

#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)

#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     return creds

# # ------------------------
# # SEND EMAIL TOOL
# # ------------------------
# def send_email(to: str, subject: str, body: str):
#     creds = get_creds()
#     service = build("gmail", "v1", credentials=creds)

#     message = EmailMessage()
#     message.set_content(body)
#     message["To"] = to
#     message["Subject"] = subject

#     encoded_message = base64.urlsafe_b64encode(
#         message.as_bytes()
#     ).decode()

#     service.users().messages().send(
#         userId="me",
#         body={"raw": encoded_message}
#     ).execute()

#     return "Email sent successfully."

# # ------------------------
# # CREATE CALENDAR INVITE TOOL
# # ------------------------
# def create_calendar_invite(
#     title: str,
#     description: str,
#     start_time: str,
#     end_time: str
# ):
#     creds = get_creds()
#     service = build("calendar", "v3", credentials=creds)

#     event = {
#         "summary": title,
#         "description": description,
#         "start": {
#             "dateTime": start_time,
#             "timeZone": "Asia/Kolkata",
#         },
#         "end": {
#             "dateTime": end_time,
#             "timeZone": "Asia/Kolkata",
#         },
#     }

#     service.events().insert(
#         calendarId="primary",
#         body=event
#     ).execute()

#     return "Calendar invite created successfully."




# import os
# import base64
# from email.message import EmailMessage

# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials

# # ------------------------
# # SCOPES
# # ------------------------
# SCOPES = [
#     "https://www.googleapis.com/auth/gmail.send",
#     "https://www.googleapis.com/auth/calendar.events",
# ]

# # ------------------------
# # AUTH HELPER
# # ------------------------
# def get_creds():
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)

#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     return creds

# # ------------------------
# # SEND EMAIL
# # ------------------------
# def send_email(to: str, subject: str, body: str):
#     creds = get_creds()
#     service = build("gmail", "v1", credentials=creds)

#     message = EmailMessage()
#     message.set_content(body)
#     message["To"] = to
#     message["Subject"] = subject

#     encoded_message = base64.urlsafe_b64encode(
#         message.as_bytes()
#     ).decode()

#     service.users().messages().send(
#         userId="me",
#         body={"raw": encoded_message}
#     ).execute()

#     return "Email sent successfully."

# # ------------------------
# # EMAIL NODE WRAPPER
# # ------------------------
# def send_email_node(state):
#     # FIX: Use .get() with defaults to prevent KeyError
#     to = state.get("to")
#     subject = state.get("subject", "No Subject")
#     body = state.get("body", "")
    
#     if not to:
#         state["response"] = "Email not sent: no recipient."
#         return state

#     send_email(to, subject, body)
#     state["response"] = "Email sent successfully."
#     return state

# # ------------------------
# # CREATE CALENDAR INVITE
# # ------------------------
# def create_calendar_invite(title: str, description: str, start_time: str, end_time: str):
#     creds = get_creds()
#     service = build("calendar", "v3", credentials=creds)

#     event = {
#         "summary": title,
#         "description": description,
#         "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
#         "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
#     }

#     service.events().insert(calendarId="primary", body=event).execute()
#     return "Calendar invite created successfully."



# COMPLETE WORKING CODE - NO MORE KEYERROR

# tools.py
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

def get_creds():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def send_email(to: str, subject: str, body: str):
    creds = get_creds()
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()
    message.set_content(body)
    message["To"] = to
    message["Subject"] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": encoded_message}).execute()
    return "Email sent successfully."

# ✅ FIXED send_email_node - ALWAYS returns new dict
def send_email_node(state):
    to = state.get("to")
    subject = state.get("subject", "No Subject")
    body = state.get("body", "")
    
    if not to:
        return {"response": "Email not sent: no recipient."}
    
    send_email(to, subject, body)
    return {"response": "✅ Email sent successfully!"}

def create_calendar_invite(title: str, description: str, start_time: str, end_time: str):
    creds = get_creds()
    service = build("calendar", "v3", credentials=creds)
    event = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
    }
    service.events().insert(calendarId="primary", body=event).execute()
    return "Calendar invite created successfully."
