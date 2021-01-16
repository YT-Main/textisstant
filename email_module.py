import smtplib
import time
import imaplib
import email
import traceback
import configparser
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

class Gmail:
    def __init__(self):
        self.ORG_EMAIL = "@gmail.com"
        self.FROM_EMAIL = "nathaniel.hawthorn96" + self.ORG_EMAIL
        self.FROM_PWD = "HacktheNorth2021"
        self.SMTP_SERVER = "imap.gmail.com"
        self.SMTP_PORT = 993

    def find_encoding_info(self, txt):
        info = email.header.decode_header(txt)
        s, encoding = info[0]
        return s, encoding

    def _read_email(self, mail, email_id, whitelist):
        try:
            data = mail.fetch(str(email_id), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    email_message = email.message_from_string(str(arr[1],'utf-8'))
                    sender = email_message['From']
                    if any(address in sender for address in whitelist):
                        email_dict = {}
                        email_dict['sender'] = email_message['From']
                        email_dict['date'] = email_message['Date']

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

                        return email_dict
                    else:
                        return None

        except Exception as e:
            print("Fatal Error")
            traceback.print_exc()
            print(str(e))

    def read_latest_emails(self, whitelist, n_emails_before=100):
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
                mail_content = self._read_email(mail, i, whitelist)
                if mail_content is not None:
                    whitelist_emails.append(mail_content)

            return whitelist_emails

        except Exception as e:
            print("Fatal Error")
            traceback.print_exc() 
            print(str(e))
            return None


gmail = Gmail()

emails = gmail.read_latest_emails(['Facebook'])
# gmail.read_all_email_from_gmail()

