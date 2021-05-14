import os
from twilio.rest import Client

# Fetching env vars
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
from_wa = os.environ.get('TWILIO_FROM_CONTACT')


class Notify:
    def __init__(self):
        self.client = Client(twilio_account_sid, twilio_auth_token)

    def send_whatsapp(self, contact, message):
        client = self.client

        client.messages.create(
            body=message, from_=from_wa, to='whatsapp:'+str(contact))
