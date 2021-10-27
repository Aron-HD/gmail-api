import logging
from dataclasses import dataclass
from typing import Dict, Union, List, Optional
from abc import ABC, abstractmethod

from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

log = logging.getLogger(__name__)


class Message(ABC):
    """Strategy for retrieving the data required for the message."""
    to: Union[List[str], str]
    subject: str
    body_text: str
    sender: str
    cc: Optional[Union[List[str], str]]
    bcc: Optional[Union[List[str], str]]

    @abstractmethod
    def create(self):
        pass


@dataclass
class BaseMessage(Message):

    to: Union[List[str], str]
    subject: str
    body_text: str = None
    sender: str = 'me'
    cc: Optional[Union[List[str], str]] = None
    bcc: Optional[Union[List[str], str]] = None

    def set_headers(self, msg):
        for k, v in self.__dict__.items():
            if v != None:
                msg[k] = v

    def create(self):
        msg = MIMEText(self.body_text)
        self.set_headers(msg)
        raw_msg = urlsafe_b64encode(msg.as_string().encode("utf-8"))
        return {'raw': raw_msg.decode("utf-8")}


class MultiPartMessage(BaseMessage):
    # pass these in as params

    def create(self, plain_txt, html_txt):
        msg = MIMEMultipart("alternative")
        p1 = MIMEText(plain_txt, 'plain')
        p2 = MIMEText(html_txt, 'html')
        self.set_headers(msg)
        # print(msg)
        # attach parts
        for p in [p1, p2]:
            msg.attach(p)

        raw_message = urlsafe_b64encode(msg.as_string().encode("utf-8"))
        return {'raw': raw_message.decode("utf-8")}
