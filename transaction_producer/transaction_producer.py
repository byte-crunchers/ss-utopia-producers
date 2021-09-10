import random
import traceback
import datetime
from faker import Faker
import sys
from connection_helper import connect
from jaydebeapi import Error

#class Timer:
#    def __init__(self, step):
#        self.step = step
#        self.intime = time.perf_counter()
#    def end(self):
#        print("{step} took {time:f} seconds".format(step=self.step, time=time.perf_counter() - self.intime))

country_codes = ("US", "VI", "VN", "ZA", "TJ", "TH", "TD", "SY", "SO", "SJ", "RU", "PS", "NG", "MX", "KR", "KP", "JP", "GU", "MP", "CN", "CA", "AS")

class Transaction:
    def __init__(self, fake, account_a, account_b,):
        self.origin_accounts_id = account_a
        self.destination_accounts_id = account_b
        self.memo = fake.text(255)
        self.transfer_value = random.random()*2000.00
        self.time_stamp = datetime.datetime.now()

class Card_Transaction:
    def __init__(self, fake, card_num, account, pin=None,cvc1=None,cvc2=None):
        self.card_num = card_num
        self.merchant_account_id = account
        self.memo = fake.text(255)
        self.transfer_value = random.random()*2000.00
        self.pin = pin
        self.cvc1 = cvc1
        self.cvc2 = cvc2
        self.time_stamp = datetime.datetime.now()
        self.location = random.choice(country_codes)
        
def get_accounts(conn):
    cur = conn.cursor()
    query = 'SELECT id FROM accounts'
    cur.execute(query)
    return cur.fetchall()

def get_cards(conn):
    cur = conn.cursor()
    query = 'SELECT card_num, pin, cvc1, cvc2 FROM cards'
    cur.execute(query)
    return cur.fetchall()

   
def generate_transactions(num_rows, conn):
    accounts = get_accounts(conn)
    if (len(accounts) == 0):
        print("ERROR: missing accounts from database")
        return 1
    query = 'INSERT INTO transactions(origin_account, destination_account, memo, transfer_value, time_stamp) VALUES (?,?,?,?,?)'
    fake = Faker() #this takes about 30ms, so it must be removed from the loop
    cur = conn.cursor()
    for i in range (num_rows):
        accounts_sample = random.sample(accounts, 2) #use so that we can have two random, unique accounts
        trans = Transaction(fake, accounts_sample[0][0], accounts_sample[1][0])
        vals = (trans.origin_accounts_id, trans.destination_accounts_id, trans.memo, trans.transfer_value, trans.time_stamp.__str__())
        try:
            cur.execute(query, vals)
        except Error:
            print("There was a problem writing to the database.")
            traceback.print_exc()
    conn.commit()

def generate_card_transactions(num_rows, conn):
    accounts = get_accounts(conn)
    cards = get_cards(conn)
    if (len(accounts) == 0 or len(cards) == 0):
        print("ERROR: missing data from database")
        return 1
    query = 'INSERT INTO card_transactions(card_num, merchant_account_id, memo, transfer_value, pin, cvc1, cvc2, location, time_stamp) VALUES (?,?,?,?,?,?,?,?,?)'
    fake = Faker() #this takes about 30ms, so it must be removed from the loop
    cur = conn.cursor()
    for i in range (num_rows):
        account = random.choice(accounts)
        card = random.choice(cards)
        trans = Card_Transaction(fake, card[0], account[0], pin=card[1])
        if random.random() < 0.25: #1/4 chance of a mag-swipe, 1/4 its amazon, 2/4 online/phone transaction from a reputable store
            trans.cvc1 = card[2]
        elif random.random() <0.33:
            pass #amazon does not use cvc because they don't care about the consumer
        else:
            trans.cvc2 = card[3]
        vals = (trans.card_num, trans.merchant_account_id, trans.memo, trans.transfer_value, trans.pin, trans.cvc1, trans.cvc2, trans.location, trans.time_stamp.__str__())
        try:
            cur.execute(query, vals)
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()
    conn.commit()


    

def clear_trans(conn):
    cur = conn.cursor()
    query = 'DELETE FROM transactions'
    cur.execute(query)
    #doesn't commit until the generate function
    
    
def clear_card_trans(conn):
    cur = conn.cursor()
    query = 'DELETE FROM card_transactions'
    cur.execute(query)
    #doesn't commit until the generate function
    

if __name__ == '__main__':
    trans_num =  int(sys.argv[1])
    card_num = int(sys.argv[2])
    conn = connect()
    clear_trans(conn)
    generate_transactions(trans_num, conn)
    clear_card_trans(conn)
    generate_card_transactions(card_num, conn)
    conn.close()