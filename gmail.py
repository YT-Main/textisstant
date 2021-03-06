import smtplib
import time
import imaplib
import email
import traceback
import configparser

class Gmail:
    def __init__(self):
        self.ORG_EMAIL = "@gmail.com"
        self.FROM_EMAIL = "nathaniel.hawthorn96" + self.ORG_EMAIL
        self.FROM_PWD = "HacktheNorth2021"
        self.SMTP_SERVER = "imap.gmail.com"
        self.SMTP_PORT = 993
        self.whitelist = []

    def find_encoding_info(self, txt):
        info = email.header.decode_header(txt)
        s, encoding = info[0]
        return s, encoding

    def _read_email(self, mail, email_id):
        try:
            data = mail.fetch(str(email_id), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    email_message = email.message_from_string(str(arr[1],'utf-8'))
                    sender = email_message['From']
                    if any(address in sender for address in self.whitelist):
                        email_dict = {}
                        email_dict['sender'] = email_message['From']

                        subject, encode = self.find_encoding_info(email_message['Subject'])

                        message = ''

                        if email_message.is_multipart():
                            for part in email_message.get_payload():
                                if part.get_content_type() == 'text/plain':
                                    bytes = part.get_payload(decode=True)
                                    encode = part.get_content_charset()
                                    message = message + str(bytes, encode)
                        else:
                            if email_message.get_content_type() == 'text/plain':
                                bytes = email_message.get_payload(decode=True)
                                encode = email_message.get_content_charset()
                                message = str(bytes, encode)
                        email_dict['msg'] = message

                        email_content = email_dict['sender'] + '\n\n' + email_dict['msg']

                        return email_content
                    else:
                        return None

        except Exception as e:
            print("Fatal Error")
            traceback.print_exc()
            print(str(e))

    def read_latest_emails(self, n_emails_before=10):
        try:
            mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
            mail.login(self.FROM_EMAIL, self.FROM_PWD)
            mail.select('inbox')

            data = mail.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()[-n_emails_before:]

            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            whitelist_emails = []

            for i in range(latest_email_id, first_email_id, -1):
                mail_content = self._read_email(mail, i)
                if mail_content is not None:
                    whitelist_emails.append(mail_content)

            if len(whitelist_emails) == 0:
                return None
            else:
                return whitelist_emails[0]

        except Exception as e:
            print("Fatal Error")
            traceback.print_exc() 
            print(str(e))
            return None

    def add_whitelist(self, whitelist_sender):
        self.whitelist.append(whitelist_sender)

# Created By: Younghoon Kim (AKA Brian Kim)