import random
import traceback
import json
import datetime
import jaydebeapi
from jaydebeapi import Error

def connect():
    con_try = None
    try:
        f = open('../dbkey.json', 'r')
        key = json.load(f)        
        con_try = jaydebeapi.connect(key["driver"], key["location"], key["login"], key["jar"] )
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    return con_try


class Account:
    def __init__(self):
            self.user = None
            self.account_type = None
            self.balance = None
            self.payment_due = None
            self.due_date = None
            self.limit = None

def get_users(conn):
    cur = conn.cursor()
    query = "SELECT id FROM users"
    cur.execute(query)
    return cur.fetchall()

def get_account_types(conn):
    cur = conn.cursor()
    query = "SELECT id FROM account_types"
    cur.execute(query)
    return cur.fetchall()


def create_account(user, account_type): #takes user account number, returns account object
    account = Account()
    account.user = user
    account.account_type = account_type
    if (account_type == "Checking" or account_type == "Savings"): #non-loan accounts
        account.balance = random.uniform(0, 4206.9)
        account.payment_due = 0
    else:
        account.limit = random.uniform(-4206.9, 0)
        account.balance = random.uniform(account.limit, 0)
        account.payment_due = account.balance * -0.10 #pay 10%
        account.due_date = datetime.date.today() + datetime.timedelta(days = random.randrange(1,31))
    return account
    
def generate(num_rows, conn):
    users_all = get_users(conn)
    if (len(users_all) < num_rows//2+1):
        print ("Not enough users in the database to support that many rows \n"\
            +"The database only supports {:d} rows".format(len(users_all) * 2 - 1))
        return 1
    users = random.sample(users_all, num_rows//2+1) #gets a random sampling of users
                                                #//2 means the average user will have two accounts 
    query = 'INSERT INTO accounts(users_id, account_type, balance, payment_due, due_date, "limit") VALUES (?,?,?,?,?,?)'
    acc_types = get_account_types(conn)
    cur = conn.cursor()
    for i in range (num_rows):
        account = create_account(random.choice(users)[0], random.choice(acc_types)[0]) #takes a random user id and account type
        vals = (account.user, account.account_type, account.balance, account.payment_due,\
         date_to_string(account.due_date), account.limit)
        try:
            cur.execute(query, vals)
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()

    conn.commit()

def date_to_string(date): #differs from str(date) in that it accepts none
    if date:
        return str(date)
    return None

def clear(conn):
    cur = conn.cursor()
    query = "DELETE FROM accounts"
    cur.execute(query)
    #doesn't commit until the generate function