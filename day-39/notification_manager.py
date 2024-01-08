from twilio.rest import Client
import config

ACCOUNT_SID = config.ACCOUNT_SID
AUTH_TOKEN = config.AUTH_TOKEN
TWILIO_NUMBER = config.TWILIO_NUMBER
TWILIO_SEND_TO_NUMBER = config.TWILIO_SEND_TO_NUMBER


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""
    def __init__(self) -> None:
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_notification(self, message):
        message = self.client.messages.create(
            from_=TWILIO_NUMBER,
            body=message,
            to=TWILIO_SEND_TO_NUMBER,
        )

       # print(message.sid)
