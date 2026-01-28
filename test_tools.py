from tools import send_email, create_calendar_invite

# Test Gmail
send_email(
    to="arbindkumarroy87@gmail.com",
    subject="Milestone 4 Test Email",
    body="This is a real Gmail API test email..."
)

# Test Calendar
create_calendar_invite(
    title="Milestone 4 Test Meeting",
    description="Test calendar invite",
    start_time="2026-01-29T10:00:00",
    end_time="2026-01-29T10:30:00"
)
