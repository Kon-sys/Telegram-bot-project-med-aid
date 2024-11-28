from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP
import os

#sablzrwaegfagnlc
#This script sends email using an asynchronous SMTP client.
#Gets email and password from environment variables. If the variables are not set, the default values ​​are used:
# - EMAIL: 'likhtar.i@yandex.by'
# - PWD: 'sablzrwaegfagnlc'
#Function `send_mail(subject, to, msg)`:
# - Creates a multipart message with the specified subject, recipient address, and HTML content.
# - Connects to the Yandex SMTP server to send email.
# - Logs in using the provided credentials and sends a message.
# - Processes possible errors and displays appropriate notifications.
#The script is run using the `asyncio.run()` function, which triggers an email to be sent on startup.
EMAIL = os.getenv('YANDEX_EMAIL', 'likhtar.i@yandex.by')
PWD = os.getenv('YANDEX_PASSWORD', 'sablzrwaegfagnlc')

async def send_mail(subject, to, msg):
    message = MIMEMultipart()
    message["From"] = EMAIL
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(f"<html><body>{msg}</body></html>", "html", "utf-8"))

    smtp_client = SMTP(hostname="smtp.yandex.by", port=465, use_tls=True)
    try:
        async with smtp_client:
            await smtp_client.login(EMAIL, PWD)
            await smtp_client.send_message(message)
            print("Email отправлен успешно!")
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")
