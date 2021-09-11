import datetime
import random
import json
import jaydebeapi
import traceback
from jaydebeapi import Error

def connect():
    con_try = None
    try:
        key = json.load(open('../dbkey.json', 'r'))        
        con_try = jaydebeapi.connect(key["driver"], key["location"], key["login"], key["jar"] )
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    return con_try

class Loan:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.balance = random.random() * -400000.00 #chooses a random balance between 0 and -400k
        self.interest_rate = random.random() * 0.05 + 0.03 #random rate between 0.03 and 0.08
        self.due_date = datetime.date.today() + datetime.timedelta(days = random.randrange(1,31))
        self.payment_due = self.balance * self.interest_rate * -0.5 #basically just pay 6x the interest rate

def get_users(conn):
    cur = conn.cursor()
    query = "SELECT id FROM users"
    cur.execute(query)
    return cur.fetchall()

def generate_loans(num_rows, conn):
    users = get_users(conn)
    query = 'INSERT INTO loans(users_id, balance, interest_rate, due_date, payment_due) VALUES (?,?,?,?,?)'
    cur = conn.cursor()
    for i in range (num_rows):
        loan = Loan(random.choice(users)[0]) #takes a random user id
        vals = (loan.user_id, loan.balance, loan.interest_rate, str(loan.due_date), loan.payment_due)
        cur.execute(query, vals)

def clear(conn):
    cur = conn.cursor()
    query = "DELETE FROM loans"
    cur.execute(query)
    #doesn't commit until the generate function