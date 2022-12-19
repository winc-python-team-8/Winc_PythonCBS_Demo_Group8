import logging
import sqlite3
import CBS_DataAccess.Helper as h
import csv
import CBS_UtilityMethods.UtilityMethods as utility


class DataAccess:
    def __init__(self, dbname):
        self.dbname = dbname
        # connecting to the DB
        # TODO: add condition to not create DB if already exists as safe check.
        self.connection = sqlite3.connect(self.dbname)

        # creating a cursor for insert and select operation
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_query = h.create_table()
        # creating table into DB
        self.cursor.execute(create_table_query)
        self.connection.commit()

    # inserting data into the database from csv file.
    def insert_database(self, csvfile):
        insert_query = h.insert_table()
        if utility.is_file_valid(csvfile):
            # TODO: update the csv file name during code integration
            with open(csvfile, 'r') as file:
                csvfile_data = csv.reader(file)
                self.cursor.executemany(insert_query, csvfile_data)
        else:
            logging.warning('File does not exist or file is empty!! No data may get inserted in DB!!')
        self.connection.commit()

    # to add new columns 'flag' and 'email' in the table
    def alter_table(self):
        list_alter_queries = h.update_table()
        for query in list_alter_queries:
            self.cursor.execute(query)
        self.connection.commit()

    # to update the flag column for the duplicate transaction ids
    def update_duplicates(self):
        duplicate_query = h.get_duplicates()
        duplicates = self.cursor.execute(duplicate_query).fetchall()
        if len(duplicates) > 0:
            list_trans_id = []
            for i in range(len(duplicates)):
                list_trans_id.append(duplicates[i][0])
            update_duplicate_query = h.update_duplicates(list_trans_id)
            self.cursor.execute(update_duplicate_query)
            logging.info('Total number of duplicate records found and updated are: {0}'.format(len(duplicates)))
        else:
            logging.warning('No records found with duplicate transaction ids')
        self.connection.commit()

    # get all transaction ids where operation is null or  and update the flag value
    def update_suspicious_records(self):
        get_suspicious_operations_query = h.get_suspicious_records()
        suspicious_operations = self.cursor.execute(get_suspicious_operations_query).fetchall()
        if len(suspicious_operations) > 0:
            list_susp_trans_id = []
            for i in range(len(suspicious_operations)):
                list_susp_trans_id.append(suspicious_operations[i][0])
            update_suspicious_query = h.update_suspicious_records(list_susp_trans_id)
            self.cursor.execute(update_suspicious_query)
            logging.info('Total number of suspicious records found and updated are: {0}'.format(len(suspicious_operations)))
        else:
            logging.warning('No suspicious records found with empty operations')

        self.connection.commit()

    # to get the max trans_id for a particular account holder
    def get_pensioner_max_trans_id(self):
        max_trans_id_query = h.get_max_trans_id()
        max_trans_id = self.cursor.execute(max_trans_id_query).fetchall()
        self.connection.commit()
        return max_trans_id

    # to update the balance of the account holders who are above 60 years of age
    def credit_interest(self, list_max_trans_id):
        credit_interest_query = h.credit_interest(list_max_trans_id)
        credit_interest = self.cursor.execute(credit_interest_query).fetchall()
        if len(credit_interest) > 0:
            logging.info('Total number of records where interest is credited are: {0}'.format(len(credit_interest)))
        else:
            logging.warning('No records found for account holders above 60 years of age')
        self.connection.commit()

    # to get all the transaction ids where the pensioner bonus was credited so csv file can be created
    def get_pensioner_details(self):
        get_pensioner_query = h.get_pensioner_details()
        pensioner_data = self.cursor.execute(get_pensioner_query).fetchall()
        self.connection.commit()
        return pensioner_data

    # to get the list of trans_id where current balance is less than 800
    def get_account_trans_id(self):
        account_trans_id_query = h.get_account_trans_id_query()
        account_trans_id = self.cursor.execute(account_trans_id_query).fetchall()

        self.connection.commit()
        return account_trans_id

    def update_email_id_details(self, list_account_id):
        list_email_update_queries = h.update_email_id_details(list_account_id)
        for query in list_email_update_queries:
            self.cursor.execute(query)
        self.connection.commit()

# to get details of all account id, balance and email ids where balance is less than 800 so mail can be sent
    def get_account_email_details(self, list_trans_id):
        account_email_details_query = h.get_account_email_details_query(list_trans_id)
        account_email_details = self.cursor.execute(account_email_details_query).fetchall()
        self.connection.commit()
        return account_email_details

# to get the details of cash type transactions and their count and year as well
    def get_cash_transactions_details(self):
        cash_transactions_query = h.get_cash_transactions_query()
        cash_transaction_details = self.cursor.execute(cash_transactions_query).fetchall()
        self.connection.commit()
        return cash_transaction_details

# to get total transactions count to calculate digital/cash ratio
    def get_total_transaction_details(self):
        total_transaction_query = h.get_total_transaction_query()
        total_transaction_count = self.cursor.execute(total_transaction_query).fetchall()
        self.connection.commit()
        return total_transaction_count

# to get total digital transactions count to calculate digital/cash ratio
    def get_total_digital_transactions_details(self):
        total_digital_transaction_query = h.get_total_digital_transactions_query()
        print(total_digital_transaction_query)
        total_digital_transaction_count = self.cursor.execute(total_digital_transaction_query).fetchall()
        self.connection.commit()
        return total_digital_transaction_count

# update bank account mappings in the table
    def get_digital_cash_count_details(self):
        digital_cash_count_query = h.get_digital_cash_count_details_query()
        # print(update_bank_account_mapping_query)
        digital_cash_count_details = self.cursor.execute(digital_cash_count_query).fetchall()
        self.connection.commit()
        return digital_cash_count_details

# to get total cash transactions count to calculate digital/cash ratio
    def get_total_cash_transactions_query(self):
        total_cash_transactions_query = h.get_total_cash_transactions_query()
        total_cash_transactions_count = self.cursor.execute(total_cash_transactions_query).fetchall()
        self.connection.commit()
        return total_cash_transactions_count

    def close_connection(self):
        self.connection.close()
