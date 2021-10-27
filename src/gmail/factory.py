import logging
import pandas as pd
from pprint import pprint
from jinja2 import Environment, FileSystemLoader

from gmail.app import App, Gmail
from gmail.message import Message, BaseMessage, MultiPartMessage

log = logging.getLogger(__name__)


class MailFactory:
    """Class responsible for creating messages and operating Gmail App."""

    def __init__(self, app: App):
        self.app = app

    def create_raw_msg(self, header):

        m = BaseMessage(**header)
        return m.create()

    def create_raw_multi(self, header, txt, html):

        m = MultiPartMessage(**header)
        return m.create(txt, html)

    def create_draft(self, msg) -> str:
        """Creates a draft from the raw message object"""
        draft = self.app.create_draft(msg)
        return draft

    def send_draft(self, draft) -> str:
        """Creates a draft from the raw message object"""
        self.app.send_draft(draft)
        return draft

    def delete_draft(self, msg_id):
        return self.app.delete_draft(str(msg_id))

    def send_message_directly(self, msg):
        message = self.app.send_message(msg)
        print(f'sent message: {message["id"]}')
        return message['id']


# Jinja Imports
env = Environment(
    loader=FileSystemLoader('./src/templates'))


class DataHandler:

    def render_template(tmpl, data):
        return env.get_template(str(tmpl)).render(d=data)

    def get_text(src):
        with open(src) as f:
            return f.read()

    def process_csv_data(email_list):
        df = pd.read_csv(email_list).fillna(False)
        return df.to_dict('records')

    def run(factory: MailFactory, d):

        header = {
            "subject": f"WMA - {d['category']} shortlist pdfs",
        }
        try:
            [
                header.update({k: d[k]})
                for k in ('to', 'cc', 'bcc') if d[k]
            ]
        except KeyError as e:
            log.error(e)

        txt_file = DataHandler.render_template('shortlist-pdfs.txt', data=d)
        html_file = DataHandler.render_template('shortlist-pdfs.html', data=d)

        # msg1 = fac.create_raw_msg(header=test_raw_msg_header)
        msg = factory.create_raw_multi(
            header=header,
            txt=txt_file,
            html=html_file
        )

        draft = factory.create_draft(msg)

        return (f"{d['name']} {d['surname']}", draft)


def main():

    app = Gmail()
    fac = MailFactory(app)

    file = './src/data/shortlist-groups.csv'
    # file = './src/data/test-data.csv'
    csv_data = DataHandler.process_csv_data(file)

    msgs = list()
    for d in csv_data:
        draft = DataHandler.run(fac, d)
        msgs.append(draft)

    if input('\ndelete all drafts? y/n: ') == 'y':
        for k, v in msgs:
            fac.delete_draft(v['id'])
            pprint(f"deleted: {k} > {v['id']}")
    else:
        if input('\nsend all drafts? y/n: ') == 'y':
            for k, v in msgs:
                pprint(f"sent: {k} > {v['id']}")
                fac.send_draft(v)


if __name__ == '__main__':
    main()
