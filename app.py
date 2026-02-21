import streamlit as st
import re
from datetime import datetime, timedelta

from gmail_service import fetch_unread_email, send_reply, create_calendar_event
from triage import triage
from agent import agent
from memory import load_memory, update_memory


# Ensure owner name exists
memory = load_memory()
if "owner_name" not in memory:
    update_memory("owner_name", "Bob")


st.set_page_config(page_title="Ambient Email Assistant", layout="wide")

st.title("📧 Ambient AI Email Assistant")
st.markdown("Stateful Autonomous Email Agent with Memory + Calendar + HITL")


if "current_email" not in st.session_state:
    st.session_state.current_email = None

if "draft_reply" not in st.session_state:
    st.session_state.draft_reply = None


def extract_time(text):
    text = text.lower()

    if "tomorrow" in text:
        match = re.search(r"(\d{1,2})\s*(am|pm)", text)
        if match:
            hour = int(match.group(1))
            period = match.group(2)

            if period == "pm" and hour != 12:
                hour += 12
            if period == "am" and hour == 12:
                hour = 0

            meeting_date = datetime.now() + timedelta(days=1)
            meeting_date = meeting_date.replace(
                hour=hour, minute=0, second=0, microsecond=0
            )

            end_time = meeting_date + timedelta(hours=1)

            return meeting_date.isoformat(), end_time.isoformat()

    return None, None


if st.button("📥 Fetch Unread Email"):

    email = fetch_unread_email()

    if not email:
        st.warning("No unread emails found.")
    else:
        st.session_state.current_email = email
        st.session_state.draft_reply = None
        st.success("Email fetched successfully.")


if st.session_state.current_email:

    email = st.session_state.current_email

    st.subheader("📨 Incoming Email")
    st.write("**Subject:**", email["subject"])
    st.write("**From:**", email["sender"])

    decision = triage(email["body"])

    st.subheader("🧠 Triage Decision")
    st.write(decision.upper())

    if decision == "ignore":
        from gmail_service import move_to_spam
        move_to_spam(email["id"])
        st.error("Spam detected. Email moved to Spam folder automatically.")

    elif decision == "notify":
        st.info("Human attention required. No automatic reply.")

    elif decision == "respond":

        sender_raw = email["sender"]
        sender_name = sender_raw.split("<")[0].strip()

        state = {
            "email": email["body"],
            "threadId": email["threadId"],
            "sender_name": sender_name
        }

        result = agent.invoke(state)
        st.session_state.draft_reply = result["draft"]


if st.session_state.draft_reply:

    st.subheader("✍️ Draft Reply")

    edited_reply = st.text_area(
        "Edit reply if needed:",
        value=st.session_state.draft_reply,
        height=200
    )

    email = st.session_state.current_email

    start_time, end_time = extract_time(email["body"])

    create_event = False

    if start_time and end_time:
        st.info("📅 Time detected in email.")
        create_event = st.checkbox("Create Calendar Event")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve & Send"):

            if create_event:
                create_calendar_event(
                    "Client Meeting",
                    start_time,
                    end_time
                )
                st.success("Calendar event created.")

            send_reply(
                email["threadId"],
                email["sender"],
                "Re: " + email["subject"],
                edited_reply
            )

            st.success("Reply sent successfully.")

    with col2:
        if st.button("❌ Deny"):
            st.warning("Reply cancelled.")


st.subheader("💾 Persistent Memory")
memory = load_memory()
st.json(memory)