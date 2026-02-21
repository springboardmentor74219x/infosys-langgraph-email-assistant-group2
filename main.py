import re
from datetime import datetime, timedelta

from gmail_service import (
    fetch_unread_email,
    send_reply,
    create_calendar_event,
    move_to_spam
)
from triage import triage
from agent import agent
from memory import load_memory, update_memory


# ----------------------------------------
# Ensure owner name exists in memory
# ----------------------------------------
memory = load_memory()
if "owner_name" not in memory:
    update_memory("owner_name", "Bob")


# ----------------------------------------
# Helper: Extract Meeting Time
# ----------------------------------------
def extract_time(email_text):

    email_text = email_text.lower()

    if "tomorrow" in email_text:
        match = re.search(r'(\d{1,2})\s*(am|pm)', email_text)

        if match:
            hour = int(match.group(1))
            period = match.group(2)

            if period == "pm" and hour != 12:
                hour += 12
            if period == "am" and hour == 12:
                hour = 0

            if hour < 0 or hour > 23:
                return None, None

            meeting_date = datetime.now() + timedelta(days=1)
            meeting_date = meeting_date.replace(
                hour=hour,
                minute=0,
                second=0,
                microsecond=0
            )

            end_time = meeting_date + timedelta(hours=1)

            return meeting_date.isoformat(), end_time.isoformat()

    return None, None


# ----------------------------------------
# MAIN EXECUTION LOOP
# ----------------------------------------
def run():

    print("\n🔵 Ambient Email Assistant Running...\n")

    email = fetch_unread_email()

    if not email:
        print("⚠️ No unread emails found.")
        return

    print("📨 Email received")
    print("Subject:", email["subject"])
    print("From:", email["sender"])

    decision = triage(email["body"])

    print("\n🧠 Triage Decision:", decision.upper())

    if decision == "ignore":
        move_to_spam(email["id"])
        print("🚫 Spam detected. Moved to Spam folder.")
        return

    elif decision == "notify":
        print("🔔 Human attention required. No automatic reply.")
        return

    elif decision == "respond":

        # Extract sender name (clean format)
        sender_raw = email["sender"]
        sender_name = sender_raw.split("<")[0].strip()

        state = {
            "email": email["body"],
            "threadId": email["threadId"],
            "sender_name": sender_name
        }

        result = agent.invoke(state)

        draft_reply = result["draft"]

        print("\n✍️ Draft Reply Generated:\n")
        print(draft_reply)

        approval = input("\nApprove and send reply? (yes/no): ").strip().lower()

        if approval != "yes":
            print("❌ Reply cancelled.")
            return

        # Extract meeting time (if any)
        start_time, end_time = extract_time(email["body"])

        if start_time and end_time:
            print("📅 Meeting time detected.")
            create_event = input("Create calendar event? (yes/no): ").strip().lower()

            if create_event == "yes":
                create_calendar_event(
                    "Client Meeting",
                    start_time,
                    end_time
                )
                print("✅ Calendar event created.")

        send_reply(
            email["threadId"],
            email["sender"],
            "Re: " + email["subject"],
            draft_reply
        )

        print("✅ Reply sent successfully.")


# ----------------------------------------
# ENTRY POINT
# ----------------------------------------
if __name__ == "__main__":
    run()