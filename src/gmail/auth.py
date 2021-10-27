import logging
from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

log = logging.getLogger(__name__)


class Service:
    """Class for authenticating the app."""
    # If modifying these scopes, delete the file token.json.
    TOKEN = 'token.json'
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose',
              'https://www.googleapis.com/auth/gmail.settings.basic']

    # ToDo: can we make Scopes non specific to gmail?

    def authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if Path(self.TOKEN).exists():
            creds = Credentials.from_authorized_user_file(
                self.TOKEN, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            self.refresh_token(creds)
            # Save the credentials for the next run
            self.overwrite_token(creds)
            log.debug('refreshed token')

            # ToDo: can we make build non specific to gmail?

        return build('gmail', 'v1', credentials=creds)

    def refresh_token(self, creds):
        """Make the user log in."""
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', self.SCOPES)
            creds = flow.run_local_server(port=0)

    def overwrite_token(self, creds):
        with open(self.TOKEN, 'w') as token:
            token.write(creds.to_json())
