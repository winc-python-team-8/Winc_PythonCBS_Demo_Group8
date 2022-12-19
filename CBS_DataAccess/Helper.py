import CBS_DataAccess.Constants as c


def create_table():
    # table schema query
    create_table_query = '''CREATE TABLE {0}(
                            id          INTEGER,
                            trans_id    TEXT,
                            account_id  TEXT,
                            type        TEXT,
                            operation   TEXT,
                            amount      REAL,
                            balance     REAL,
                            k_symbol    TEXT,
                            bank        TEXT,
                            account     TEXT,
                            year        INTEGER,
                            month       INTEGER,
                            day         INTEGER,
                            fulldate    TEXT,
                            fulltime    TEXT,
                            fulldatewithtime    TEXT
                            )'''.format(c.TBL_INDIVIDUAL_PROFILES)
    return create_table_query


def insert_table():
    insert_query = "INSERT INTO {0} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(c.TBL_INDIVIDUAL_PROFILES)
    return insert_query


def update_table():
    add_flag_query = "ALTER TABLE {0} ADD COLUMN flag TEXT".format(c.TBL_INDIVIDUAL_PROFILES)
    add_email_query = "ALTER TABLE {0} ADD COLUMN email TEXT".format(c.TBL_INDIVIDUAL_PROFILES)
    update_flag_query = "UPDATE {0} SET flag = ''".format(c.TBL_INDIVIDUAL_PROFILES)
    list_alter_query = []
    list_alter_query.append(add_flag_query)
    list_alter_query.append(add_email_query)
    list_alter_query.append(update_flag_query)
    return list_alter_query


def get_duplicates():
    duplicate_query = '''SELECT trans_id,account_id, type, operation, amount, balance, k_symbol, year 
                        FROM {0} GROUP BY account_id, type, operation, amount, balance, k_symbol, year  
                        HAVING COUNT(trans_id)>1'''.format(c.TBL_INDIVIDUAL_PROFILES)
    return duplicate_query


def update_duplicates(list_trans_id):
    update_duplicate_query = '''UPDATE {0} SET flag = 'Transaction ID is duplicate!' 
                                WHERE trans_id IN ({1})
                        '''.format(c.TBL_INDIVIDUAL_PROFILES, ', '.join('\'' + item + '\'' for item in list_trans_id))
    return update_duplicate_query


def get_suspicious_records():
    get_suspicious_operations_query = '''SELECT trans_id FROM {0}
                                        WHERE operation = ''
                                        '''.format(c.TBL_INDIVIDUAL_PROFILES)
    return get_suspicious_operations_query


def update_suspicious_records(list_susp_trans_id):
    update_suspicious_query = '''UPDATE {0} SET flag = flag || ', Suspicious transaction'
                                WHERE trans_id IN ({1})
                    '''.format(c.TBL_INDIVIDUAL_PROFILES, ', '.join('\'' + item + '\'' for item in list_susp_trans_id))
    return update_suspicious_query


def get_max_trans_id():
    max_trans_id_query = '''SELECT MAX(trans_id) FROM {0}
                            WHERE k_symbol = 'Old Age Pension'
                            GROUP BY account_id                  
                        '''.format(c.TBL_INDIVIDUAL_PROFILES)
    return max_trans_id_query


def credit_interest(list_max_trans_id):
    credit_interest_query = '''UPDATE {0} SET balance = balance + balance * 0.05, 
                                flag = '' || ', Pensioner-Bonus Interest Credited' 
                                WHERE trans_id IN ({1})
                        '''.format(c.TBL_INDIVIDUAL_PROFILES, ', '.join('\''+item+'\'' for item in list_max_trans_id))
    return credit_interest_query


def get_pensioner_details():
    select_pensioner_query = '''SELECT * FROM {0}
                                WHERE flag LIKE '%Pensioner-Bonus Interest Credited%'
                               '''.format(c.TBL_INDIVIDUAL_PROFILES)
    return select_pensioner_query


def get_account_trans_id_query():
    email_trans_id_query = '''SELECT account_id, MAX(trans_id) FROM {0}
                            WHERE balance < 800 GROUP BY account_id         
                            '''.format(c.TBL_INDIVIDUAL_PROFILES)
    return email_trans_id_query


# update email ids for few records
def update_email_id_details(list_account_id):
    list_account_kd = []
    list_account_lt = []
    list_account_as = []
    for i in range(0, 5):
        list_account_kd.append(list_account_id[i])
    for i in range(5, 10):
        list_account_lt.append(list_account_id[i])
    for i in range(10, 15):
        list_account_as.append(list_account_id[i])
    update_email_id_query_kd = '''UPDATE {0} SET email = 'kidixit@deloitte.com'
                                WHERE account_id IN ({1})
                        '''.format(c.TBL_INDIVIDUAL_PROFILES, ', '.join('\'' + item + '\'' for item in list_account_kd))
    update_email_id_query_lt = '''UPDATE {0} SET email = 'kidixit@deloitte.com'
                                WHERE account_id IN ({1})
                        '''.format(c.TBL_INDIVIDUAL_PROFILES, ', '.join('\'' + item + '\'' for item in list_account_lt))
    update_email_id_query_as = '''UPDATE {0} SET email = 'adshree@deloitte.com'
                                WHERE account_id IN ({1})
                        '''.format(c.TBL_INDIVIDUAL_PROFILES, ', '.join('\'' + item + '\'' for item in list_account_as))
    list_update_email_queries =[]
    list_update_email_queries.append(update_email_id_query_kd)
    list_update_email_queries.append(update_email_id_query_lt)
    list_update_email_queries.append(update_email_id_query_as)

    return list_update_email_queries


def get_account_email_details_query(list_trans_id):
    account_email_query = '''SELECT account_id, balance, email, trans_id
                              FROM {0} WHERE trans_id IN ({1}) AND email like '%.com%'
                        '''.format(c.TBL_INDIVIDUAL_PROFILES, ', '.join('\'' + item + '\'' for item in list_trans_id))
    return account_email_query


def get_cash_transactions_query():
    cash_transactions_query = '''SELECT year, count(trans_id), 
                                        operation 
                                        FROM {0} WHERE operation IN('Credit in Cash','Cash Withdrawal','Credit Card Withdrawal')
                                        GROUP BY year, operation
                                        ORDER BY COUNT(operation) DESC'''.format(c.TBL_INDIVIDUAL_PROFILES)
    return cash_transactions_query


def get_total_transaction_query():
    total_transactions_query = '''SELECT COUNT (trans_id)
                                FROM {0} WHERE operation != ''
                                '''.format(c.TBL_INDIVIDUAL_PROFILES)
    return total_transactions_query


def get_total_digital_transactions_query():
    total_digital_transactions_query = '''SELECT bank, COUNT(DISTINCT trans_id)
                                        FROM {0} WHERE
                                        operation IN('Collection from Another Bank','Remittance to Another Bank')
                                        GROUP BY bank
                                        ORDER BY COUNT(DISTINCT trans_id) DESC
                                        '''.format(c.TBL_INDIVIDUAL_PROFILES)
    return total_digital_transactions_query


def get_digital_cash_count_details_query():
    # update_bank_account_mapping_query = '''UPDATE {0} SET a.bank = b.bank
    #                             FROM {1} a
    #                             INNER JOIN {2} b
    #                             ON a.account_id = b.account_id
    #                             WHERE b.operation IN('Collection from Another Bank')
    #                             AND a.account_id = 'A00000004' AND trans_id = 'T00001199'
    #                             '''.format(c.TBL_INDIVIDUAL_PROFILES, c.TBL_INDIVIDUAL_PROFILES, c.TBL_INDIVIDUAL_PROFILES)

    digital_cash_count_details_query = '''
                SELECT bank, type, SUM(trans_count)
                FROM
                       ( SELECT bank, CASE WHEN operation IN('Credit in Cash','Cash Withdrawal')
                                        THEN 'Cash' ELSE 'Digital' END as type, 
                        COUNT(trans_id) as trans_count
                        FROM (SELECT DISTINCT a.trans_id, a.account_id, a.operation, a.k_symbol, b.bank
                                FROM {0} a
                                LEFT JOIN {1} b
                                ON a.account_id = b.account_id
                                WHERE b.operation IN('Collection from Another Bank')                                
                             ) GROUP BY bank, operation
                        )GROUP BY bank, type ORDER BY SUM(trans_count) DESC
                                '''.format(c.TBL_INDIVIDUAL_PROFILES, c.TBL_INDIVIDUAL_PROFILES)

    # update_bank_account_mapping_query = '''
    #                         SELECT DISTINCT a.trans_id, a.account_id, a.operation, a.k_symbol, b.bank
    #                                 FROM {0} a
    #                                 LEFT JOIN {1} b
    #                                 ON a.account_id = b.account_id AND a.account_id = 'A00000004'
    #                                 WHERE b.operation IN('Collection from Another Bank')
    #                                 '''.format(c.TBL_INDIVIDUAL_PROFILES, c.TBL_INDIVIDUAL_PROFILES)
    return digital_cash_count_details_query


def get_total_cash_transactions_query():
    total_cash_transactions_query = '''SELECT count(DISTINCT trans_id)
                                        FROM {0} WHERE operation IN('Credit in Cash','Cash Withdrawal','Credit Card Withdrawal') 
                                    '''.format(c.TBL_INDIVIDUAL_PROFILES)
    return total_cash_transactions_query

