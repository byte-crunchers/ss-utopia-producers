import random
import traceback
import mysql
import json
from mysql.connector import Error
import datetime



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
    query = "SELECT id FROM account_type"
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
    query = "INSERT INTO accounts VALUES (0,%s,%s,%s,%s,%s,%s)"
    acc_types = get_account_types(conn)
    cur = conn.cursor()
    for i in range (num_rows):
        account = create_account(random.choice(users)[0], random.choice(acc_types)[0]) #takes a random user id and account type
        vals = (account.user, account.account_type, account.balance, account.payment_due,\
         account.due_date, account.limit)
        try:
            cur.execute(query, vals)
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()

    conn.commit()

def connect():
    con_try = None
    try:
        f = open('../dbkey.json', 'r')
        key = json.load(f)
        con_try = mysql.connector.connect(user=key["user"], password=key["password"], host=key["host"], database=key["database"])
        
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if con_try.is_connected():
        return con_try
    else:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
        print(Error)


def clear(conn):
    cur = conn.cursor()
    query = "DELETE FROM accounts"
    cur.execute(query)
    #doesn't commit until the generate function
    

if __name__ == '__main__':
    conn = connect()
    clear(conn)
    generate(100, conn)
    conn.close()