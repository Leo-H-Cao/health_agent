import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from health_agent.constants import EMAIL_SUBJECT_LINE, FROM_EMAIL
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OutboundEmail:
    def __init__(self):
        self.sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

    def send_appointment_email(
        self, outbound_email: str, outbound_name: str, appointment_data: dict
    ):

        provider = appointment_data.get("provider")
        date = appointment_data.get("date")
        time = appointment_data.get("time")

        message_body = f"""<strong>Hey {outbound_name}, \nYour doctor appointment with {provider} is confirmed for {date} at {time}.</strong>"""

        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=outbound_email,
            subject=EMAIL_SUBJECT_LINE,
            html_content=message_body,
        )
        try:
            logger.debug("SENDING EMAIL")
            response = self.sg.send(message)
            logger.info("Delivered email response: " + str(response.status_code))
            logger.info(response.body)
        except Exception as e:
            logger.error("Error while attempting to send email: " + e.message)
