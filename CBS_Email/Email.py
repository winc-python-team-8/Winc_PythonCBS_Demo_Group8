# Object of this class is used to write the email
import logging
from email.message import EmailMessage
# For security of email and information inside it
import ssl
# Used to send email
import smtplib
import datetime
from CBS_DataAccess.DataAccess import DataAccess
import CBS_DataAccess.Constants as dAC
import CBS_Email.Constants as eAC


class Email:
    def __init__(self, email_sender, email_password):
        self.email_sender = email_sender
        self.email_password = email_password
        self.data_access = DataAccess(dAC.DBNAME)

    # return account id balance and email details where balance is less than 800
    def get_account_trans_id_details(self):
        account_trans_id = self.data_access.get_account_trans_id()
        logging.info('Total number of accounts where current balance is less than 800: {0}'.format(len(account_trans_id)))
        list_account_id = []
        list_trans_id = []
        for i in range(len(account_trans_id)):
            list_account_id.append(account_trans_id[i][0])
        for i in range(len(account_trans_id)):
            list_trans_id.append(account_trans_id[i][1])

        # to update few email ids for sending mails.
        self.data_access.update_email_id_details(list_account_id)
        account_email_details = self.data_access.get_account_email_details(list_trans_id)
        return account_email_details

    def send_email(self, account_email_details_input):
        final_day = datetime.datetime.now() + datetime.timedelta(days=10)
        last_date = (final_day.strftime("%x"))
        # to remove any duplicate row from the list
        account_email_details = list(set([i for i in account_email_details_input]))
        logging.info('Total number of emails to be sent out: {0}'.format(len(account_email_details)))
        for account in account_email_details:
            email_receiver = account[2]
            mail_subject = eAC.EMAIL_SUBJECT
            mail_body = """Dear {0},\n
Your current balance is {1}. As per the bank policy, customers need to maintain an average minimum monthly balance of Rs.800 to keep their savings bank account active. 
\nPlease make sure you maintain the minimum balance in your account by {2} or might face a penalty.
\nThanks,
Team8 Bank
**This is a system generated mail, please do not reply.""".format(account[0], account[1], last_date)
            print('email is being sent to account recipient {0}: '.format(account[0]))
            logging.info('email is being sent to account recipient {0}: '.format(account[0]))
            mail = EmailMessage()
            mail['From'] = self.email_sender
            mail['To'] = email_receiver
            mail['Subject'] = mail_subject
            mail.set_content(mail_body)

            context = ssl.create_default_context()
            # setting connection to server
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(self.email_sender, self.email_password)
                smtp.sendmail(self.email_sender, email_receiver, mail.as_string())

            print('email sent!!')    
            logging.info('email sent!!')

