import smtplib
from email.mime.text import MIMEText

# Email parameters
sender = ""
recipient = "recipient_email_address"
subject = "Email Subject"
body = "This is the body of the email."

# SMTP server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
username = "your_email_address"
password = "your_email_password"

# Create a MIME message
message = MIMEText(body)
message["Subject"] = subject
message["From"] = sender
message["To"] = recipient

# Create a SMTP session
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(username, password)

# Send the email
server.sendmail(sender, recipient, message.as_string())

# Close the SMTP session
server.quit()