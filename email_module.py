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

    def read_email(self, email_id, whitelist):
        try:
            data = mail.fetch(str(latest_email_id), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    email_message = email.message_from_string(str(arr[1],'utf-8'))
                    print('From: ', email_message['From'])
                    print('Sender: ', email_message['Sender'])
                    print('Date: ', email_message['Date'])

                    subject, encode = self.find_encoding_info(email_message['Subject'])

                    message = ''

                    print('[Message]')
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
                    print(message)
        except Exception as e:
            print("Fatal Error")
            traceback.print_exc() 
            print(str(e))

    def read_latest_email(self):
        try:
            mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
            mail.login(self.FROM_EMAIL, self.FROM_PWD)
            mail.select('inbox')

            data = mail.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()[-20:]

            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])
            data = mail.fetch(str(latest_email_id), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    email_message = email.message_from_string(str(arr[1],'utf-8'))
                    print('From: ', email_message['From'])
                    print('Sender: ', email_message['Sender'])
                    print('Date: ', email_message['Date'])

                    subject, encode = self.find_encoding_info(email_message['Subject'])

                    message = ''

                    print('[Message]')
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
                    print(message)

        except Exception as e:
            print("Fatal Error")
            traceback.print_exc() 
            print(str(e))

    def read_all_email_from_gmail(self):
        try:
            mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
            mail.login(self.FROM_EMAIL, self.FROM_PWD)
            mail.select('inbox')

            data = mail.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            for i in range(latest_email_id,first_email_id, -1):
                data = mail.fetch(str(i), '(RFC822)' )
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1],'utf-8'))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        print('From : ' + email_from + '\n')
                        print('Subject : ' + email_subject + '\n')

        except Exception as e:
            print("Fatal Error")
            traceback.print_exc() 
            print(str(e))

gmail = Gmail()

gmail.read_latest_email()
# gmail.read_all_email_from_gmail()

