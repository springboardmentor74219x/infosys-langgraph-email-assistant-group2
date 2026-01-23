from tools import send_email_tool, create_calendar_event_tool

def test_email():
    state = {
        "response": "Test Email from Tool",
        "memory": {"to": "your_email@gmail.com"},
    }
    send_email_tool(state)
    print("Email tool working")

def test_calendar():
    state = {
        "memory": {
            "start_time": "2026-01-25T10:00:00",
            "end_time": "2026-01-25T11:00:00",
        }
    }
    create_calendar_event_tool(state)
    print("Calendar tool working")

if __name__ == "__main__":
    test_email()
    test_calendar()
