import smtplib
import csv
import json
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from logger import logger

class EmailSender:
    def __init__(self, email_address, email_password):
        self.email_address = email_address
        self.email_password = email_password

        try:
            # Set up the email server (in this case, Gmail's SMTP server)
            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()
            self.server.login(self.email_address, self.email_password)
            logger.info("Logged into Gmail Account.")

        except Exception as e:
            logger.error("Error in logging to Gmail Account.")

    def send_email(self, business_name, to_email, subject, body, attachment=None):
        # Create a message container
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(body, 'plain'))

        # Attach an optional file (e.g., a PDF)
        if attachment:
            with open(attachment, 'rb') as file:
                part = MIMEApplication(file.read(), Name='attachment.pdf')
            part['Content-Disposition'] = f'attachment; filename="{attachment}"'
            msg.attach(part)

        try:
            # Send the email
            self.server.sendmail(self.email_address, to_email, msg.as_string())
            logger.info(f"Email send to '{business_name}': '{to_email}'.")

            return True
        except Exception as e:
            logger.error(f"Error in sending email to '{business_name}': '{to_email}'.")
            return False

    def close(self):
        # Close the server connection
        self.server.quit()
        logger.info("Logged out of Gmail Account.")


if __name__ == '__main__':

    load_dotenv("credentials\.env")  # Load variables from .env file

    email_address = os.environ.get('EMAIL')
    email_password = os.environ.get('PASSWORD')

    # Create an EmailSender instance
    email_sender = EmailSender(email_address, email_password)

    email_sender.send_email(business_name="personal", to_email="mohitnilkute012@gmail.com", subject="Testing Class", body="Hello from EmailSender Python Class", attachment="Python Assignment (1).pdf")

    # Close the email server connection
    email_sender.close()
