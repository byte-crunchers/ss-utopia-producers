import datetime
import random
import traceback
import json
import jaydebeapi
from jaydebeapi import Error

def connect():
    f = open('../dbkey.json', 'r')
    key = json.load(f)        
    return jaydebeapi.connect(key["driver"], key["location"], key["login"], key["jar"] )

def get_table_id(conn, table):
    cur = conn.cursor()
    query = 'SELECT id FROM ' + table
    cur.execute(query)
    return cur.fetchall()

class Payment:
    def __init__(self, loan, account):
        self.loan_id = loan
        self.account_id = account
        self.amount = random.random()*2000.00
        self.time_stamp = datetime.datetime.now()

def generate(num_rows, conn):
    accounts = get_table_id(conn, "accounts")
    loans = get_table_id(conn, "loans")
    if (len(accounts) == 0 or len(loans) == 0):
        print("ERROR: missing accounts from database")
        raise Exception('Missing data')
    query = 'INSERT INTO loan_payments(loan_id, account_id, amount, time_stamp) VALUES (?,?,?,?)'
    cur = conn.cursor()
    for i in range (num_rows):
        pmnt = Payment(random.choice(loans)[0], random.choice(accounts)[0])
        vals = (pmnt.loan_id, pmnt.account_id, pmnt.amount, pmnt.time_stamp.__str__())
        cur.execute(query, vals)

def clear(conn):
    cur = conn.cursor()
    query = 'DELETE FROM loan_payments'
    cur.execute(query)