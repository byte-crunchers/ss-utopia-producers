import datetime
import json
import random

import jaydebeapi
from jaydebeapi import Error


def connect():
    con_try = None
    try:
        key = json.load(open('../dbkey.json', 'r'))
        con_try = jaydebeapi.connect(key["driver"], key["location"], key["login"], key["jar"])
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    return con_try


class Loan:
    def __init__(self, user_id, type) -> None:
        self.user_id = user_id
        self.balance = random.random() * -400000.00  # chooses a random balance between 0 and -400k
        self.interest_rate = random.random() * 0.05 + 0.03  # random rate between 0.03 and 0.08
        self.due_date = datetime.date.today() + datetime.timedelta(days=random.randrange(1, 31))
        self.monthly = self.balance * self.interest_rate * -0.5  # basically just pay 6x the interest rate
        self.payment_due = self.monthly * (
                    random.random() * 0.2 + 1)  # 20% jitter on monthly, for underpayment, late fees, etc
        self.type = type
        if random.random() < 0.9:  # chance the user confirmed this loan over email
            self.confirmed = True
            if random.random() < 0.9:  # chance that loan is approved
                self.approved = True
                if random.random() < 0.9:  # chance the loan hasn't been closed/suspended
                    self.active = True
                else:
                    self.active = False
            else:
                self.approved = False
                self.active = False
        else:
            self.confirmed = False
            self.approved = False
            self.active = False


def get_users(conn):
    cur = conn.cursor()
    query = "SELECT id FROM users"
    cur.execute(query)
    return cur.fetchall()


def get_loan_types(conn):
    cur = conn.cursor()
    query = "SELECT id FROM loan_types"
    cur.execute(query)
    return cur.fetchall()


def generate_loans(num_rows, conn):
    users = get_users(conn)
    types = get_loan_types(conn)
    query = 'INSERT INTO loans(users_id, balance, interest_rate, due_date, payment_due, loan_type, monthly_payment, \
        active, approved, confirmed) VALUES (?,?,?,?,?,?,?,?,?,?)'
    cur = conn.cursor()
    for i in range(num_rows):
        loan = Loan(random.choice(users)[0], random.choice(types)[0])  # takes a random user id and a random loan_type
        vals = (loan.user_id, loan.balance, loan.interest_rate, str(loan.due_date), loan.payment_due, loan.type, \
                loan.monthly, loan.active, loan.approved, loan.confirmed)
        cur.execute(query, vals)


def clear(conn):
    cur = conn.cursor()
    query = "DELETE FROM loans"
    cur.execute(query)
