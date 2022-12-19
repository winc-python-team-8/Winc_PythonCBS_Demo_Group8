import logging

from CBS_DecodeTransactionData.DecodeTransactionData import DecodeTransactionData
import CBS_DecodeTransactionData.Constants as c
from CBS_DataAccess.DataAccess import DataAccess
import CBS_DataAccess.Constants as dAC
from CBS_TransactionalDetails.Transactions import Transactions
import CBS_TransactionalDetails.Constants as tAC
from CBS_Email.Email import Email
import CBS_Email.Constants as eAC
import CBS_Logging.Logging


def run():
    logging.info('starting with transaction file decoding operation')
    file_decode = DecodeTransactionData(infile=c.INFILE, outfile=c.OUTFILE, csvfile=c.CSVFILE)
    file_decode.decode_transaction_file()
    logging.info('file is decoded successfully')

    data_access = DataAccess(dAC.DBNAME)
    data_access.create_table()
    logging.info('table is created in the database')

    # database operations
    data_access.insert_database(c.CSVFILE)
    data_access.alter_table()
    data_access.update_duplicates()
    data_access.update_suspicious_records()

    # transactions related operations
    transactions = Transactions(tAC.PENSIONER_CSVFILE, tAC.HEADER_LIST)
    transactions.credit_pensioner_bonus()
    transactions.generate_pensioner_csvfile()

    # email section
    email = Email(eAC.EMAIL_SENDER, eAC.EMAIL_PASSWORD)
    account_email_details = email.get_account_trans_id_details()
    if len(account_email_details) > 0:
        email.send_email(account_email_details)
    else:
        logging.warning('No records present with balance less than 800-No email will be sent!!')

    transactions.get_cash_transactions()
    transactions.get_digital_cash_ratio()
    print('project execution is completed')
    data_access.close_connection()


if __name__ == '__main__':
    run()



