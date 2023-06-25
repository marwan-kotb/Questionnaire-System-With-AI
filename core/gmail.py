import base64
import os.path
from email.mime.text import MIMEText

from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def send_email(to_list, subject, body):
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    # Run the flow to authorize the application and obtain an access token
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    for to in to_list:
        message = create_message(to, subject, body)
        send_message(service, message)


def create_message(to, subject, body):
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    print(f"Message 'to' field: {message['to']}")
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, message):
    try:
        message = service.users().messages().send(userId="me", body=message).execute()
    except HttpError as error:
        message = None
    return message
