import logging
from abc import ABC
from typing import Dict, Union, List, Optional

from gmail.auth import Service

log = logging.getLogger(__name__)


class App(ABC):
    pass


class Gmail(App):
    """Interface for Gmail API commands."""

    def __init__(self, user_id='me', service: Service = Service()):
        log.info('authenticating Gmail')
        self.service = service.authenticate()
        self.user_id = user_id

    def get_labels(self):
        # # Call the Gmail API
        results = self.service.users().labels().list(userId=self.user_id).execute()
        labels = results.get('labels', [])
        if not labels:
            return []
        return [label['name'] for label in labels]

    def create_draft(self, message_body):
        try:
            message = {'message': message_body}
            draft = self.service.users().drafts().create(
                userId=self.user_id, body=message).execute()
            return draft
        except Exception as e:
            log.error(e)
            return None

    def delete_draft(self, draft_id):
        try:
            self.service.users().drafts().delete(
                userId=self.user_id, id=draft_id).execute()
            return draft_id
        except Exception as e:
            log.error(e)
            return None

    def send_draft(self, draft):
        try:
            self.service.users().drafts().send(
                userId=self.user_id, body=draft).execute()
            return draft['id']
        except Exception as e:
            raise e
            return None

    def get_drafts(self):
        return self.service.users().drafts().list(
            userId=self.user_id).execute()

    def send_message(self, message_body):
        try:
            message = self.service.users().messages().send(
                userId=self.user_id, body=message_body).execute()
            return message
        except Exception as e:
            log.error(e)
            return None
