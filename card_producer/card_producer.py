import datetime
import random
import traceback
import os
import jaydebeapi
from jaydebeapi import Error

# Environment Variables
mysql_pass = os.environ.get("MYSQL_PASS")
mysql_user = os.environ.get("MYSQL_USER")
mysql_jar = os.environ.get("MYSQL_JAR")
mysql_loc = os.environ.get("MYSQL_LOC")


def connect():
    con_try = None
    try:
        con_try = jaydebeapi.connect("com.mysql.cj.jdbc.Driver", mysql_loc,
                                     [mysql_user, mysql_pass], mysql_jar)
        con_try.jconn.setAutoCommit(False)
    except Error:
        traceback.print_exc()
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    return con_try

def luhn_checksum(card_number): #shamelessly copied from SO
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-2::-2]
    even_digits = digits[-1::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return (10 - (checksum % 10)) % 10

class Card:
    def __init__(self, account):
            self.account = account
            self.num = 0 
            if(random.random() < 0.5): #50% chance user has a pin. In reality it's mostly credit cards without one
                self.pin = random.randint(1, 9998)
            else:
                self.pin = None
            self.cvc1 = random.randint(0,999)
            self.cvc2 = random.randint(0,999)
            self.exp_date = datetime.date.today() + datetime.timedelta(days = random.randrange(-80,1000))

    def build_number(self):
        left15 = '431923' + str(random.randint(0, 999999999))
                #bank id number is from Ezekiel 23:19 and Song of Soloman 2:3
                #which also works because first digit, '2', is for "airlines, financial, and other future industry assignments"
        checksum = luhn_checksum(left15)
        self.num = int(left15 + str(checksum))

def get_accounts(conn):
    cur = conn.cursor()
    query = "SELECT id FROM accounts"
    cur.execute(query)
    return cur.fetchall()

def clear(conn):
    cur = conn.cursor()
    query = "DELETE FROM cards"
    cur.execute(query)
    #doesn't commit until the generate function

def generate(num_rows, conn):
    accounts_all = get_accounts(conn)
    if (len(accounts_all) < num_rows):
        print ("ERROR: Not enough accounts in the database to support that many rows \n"\
            +"The database only has {:d} accounts".format(len(accounts_all)))
        return 1
    accounts = random.sample(accounts_all, num_rows) #gets a random sampling of accounts
                                                
    query = "INSERT INTO cards VALUES (?,?,?,?,?,?)"
    cur = conn.cursor()
    for acc in accounts:
        card = Card(acc[0])
        card.build_number()
        values = (card.account, card.num, card.pin, card.cvc1, card.cvc2, str(card.exp_date))
        try:
            cur.execute(query, values)
        except:
            # Find a unique card number that is not in the database
            while True:
                try:
                    print("collision - a 1/1,000,000,000 chance")
                    card.build_number()
                    values = (card.account, card.num, card.pin, card.cvc1, card.cvc2, str(card.exp_date))
                    cur.execute(query, values)
                    break
                except:
                    print("new number fails. That's a 1/1,000,000,000,000,000,000 chance!")
                    continue
