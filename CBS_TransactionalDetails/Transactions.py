from CBS_DataAccess.DataAccess import DataAccess
import CBS_DataAccess.Constants as dAC
import csv
import CBS_TransactionalDetails.Helper as tAH
import CBS_TransactionalDetails.Constants as tAC
import CBS_UtilityMethods.UtilityMethods as utility
import logging


class Transactions:
    def __init__(self, pensioner_csvfile, header_list):
        self.pensioner_csvfile = pensioner_csvfile
        self.header_list = header_list
        self.data_access = DataAccess(dAC.DBNAME)

    def credit_pensioner_bonus(self):
        max_trans_id = self.data_access.get_pensioner_max_trans_id()
        list_max_trans_id = []
        for i in range(len(max_trans_id)):
            list_max_trans_id.append(max_trans_id[i][0])
        self.data_access.credit_interest(list_max_trans_id)

    def generate_pensioner_csvfile(self):
        # to get all the transactions where pensioner bonus was credited and create csv file out of it
        pensioner_details = self.data_access.get_pensioner_details()
        if len(pensioner_details) > 0:
            utility.create_csv_file(self.pensioner_csvfile, self.header_list, pensioner_details)
            logging.info('''CSV file-{0} created with details of {1} pensioner bonus credited accounts
                            '''.format(self.pensioner_csvfile, len(pensioner_details)))
        else:
            logging.warning('No records found with pensioner bonus credited-CSV file will not be created')

# to get all cash type transactions and get numbers grouped by year
    def get_cash_transactions(self):
        cash_transactions_details = self.data_access.get_cash_transactions_details()
        if len(cash_transactions_details) > 0:
            utility.create_csv_file(tAC.TRANSACTIONS_CSV_FILE, tAC.TRANSACTIONS_FILE_HEADER_LIST, cash_transactions_details)
            logging.info('''CSV file-{0} created with details of preferred cash transaction types per year
                        '''.format(tAC.TRANSACTIONS_CSV_FILE))
        else:
            logging.warning('No records found with cash transaction type')

# to get transactions count to calculate digital/cash ratio
    def get_digital_cash_ratio(self):
        logging.info('Fetching Digital/Cash ratio started')
        digital_cash_ratio_details = self.data_access.get_digital_cash_count_details()        

        digital_cash_dict = dict()
        for i in range(len(digital_cash_ratio_details)):
            if digital_cash_ratio_details[i][1] == 'Digital':
                digital_cash_dict[digital_cash_ratio_details[i][0]] = digital_cash_ratio_details[i][2]
            else:
                logging.warning('No Digital transaction exists for bank: {0}'.format(digital_cash_ratio_details[i][0]))

        for i in range(len(digital_cash_ratio_details)):
            if digital_cash_ratio_details[i][0] in digital_cash_dict and digital_cash_ratio_details[i][1] == 'Cash':
                digital_cash_dict[digital_cash_ratio_details[i][0]] = digital_cash_dict[digital_cash_ratio_details[i][0]] / digital_cash_ratio_details[i][2]
            else:
                digital_cash_dict[digital_cash_ratio_details[i][0]] = digital_cash_ratio_details[i][2]
                logging.warning('No Cash transaction exists for bank: {0}'.format(digital_cash_ratio_details[i][0]))

        print('Digital/Cash Ratio per bank:')
        for key, value in digital_cash_dict.items():
            print(key, ' : ', value)
        logging.info('Fetching Digital/Cash ratio ended and details printed on console')
