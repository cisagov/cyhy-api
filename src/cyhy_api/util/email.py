import smtplib
from email.message import EmailMessage

MSG = """This is a test message.
I hope Jim isn't there."""


def send_test_email(address):
    msg = EmailMessage()
    msg.set_content(MSG)

    msg["Subject"] = f"Test message to {address}"
    msg["From"] = "cyhy@cyber.dhs.gov"
    msg["To"] = address

    # Send the message via our own SMTP server.
    s = smtplib.SMTP(host="mail", port=1025)
    s.send_message(msg)
    s.quit()
