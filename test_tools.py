from matplotlib.pyplot import title
from tools import send_email, create_calendar_invite

# Test Gmail
send_email(
    to="nikhithareddypittam@gmail.com",
    subject="Milestone 4 Test Email",
    body="This is a real Gmail API test email."
)

# Test Calendar
create_calendar_invite(
    title="Milestone 4 Test Meeting",
    description="Testing real Google Calendar API",
    start_time="2026-05-21T10:00:00",
    end_time="2026-05-21T10:30:00",
    attendees=["psinchana8@gmail.com"]
)