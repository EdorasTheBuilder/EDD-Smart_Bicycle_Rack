# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.

msg = EmailMessage()
msg.set_content('hi')

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'hello'
msg['From'] = 'smart.bike.rack.edd@gmail.com'
msg['To'] = 'rbhattaschooL@gmail.com'

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
print('msg sent')
s.quit()

