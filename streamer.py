import transaction_producer as tp
import time
import os
import sys
import json
import boto3
import random
import transaction_producer.transaction_streamer as ts
import transaction_producer.card_transaction_streamer as cs
import transaction_producer.transaction_producer as tp
import loan_payment_producer.loan_payment_streamer as ls
from faker import Faker

mask_t = 1
mask_ct = 2
mask_lp = 4
mask_stock = 8


def loopers(accounts: tuple, cards:tuple, fake: Faker, kin ) -> None:

    account = random.choice(accounts)
    card = random.choice(cards)
    trans = tp.Card_Transaction(fake, card[0], account[0], pin=card[1])
    if random.random() < 0.25: #1/4 chance of a mag-swipe, 1/4 its amazon, 2/4 online/phone transaction from a reputable store
        trans.cvc1 = card[2]
    elif random.random() <0.33:
        pass #amazon does not use cvc because they don't care about the consumer
    else:
        trans.cvc2 = card[3]

    trans.type = 'card_transaction' #for the consumer to know what type of message it is
    #print(json.dumps(trans.__dict__, default=str))
    kin.put_record(StreamName='byte-henry', Data=json.dumps(trans.__dict__, default=str), PartitionKey='card trans key')
    

def stream(options: int = 0b1111, interval: float = 5, chance: float = 1) -> None:
    conn = tp.connect()
    accounts = tp.get_accounts(conn)
    cards = tp.get_cards(conn)
    if (len(accounts) == 0 or len(cards) == 0):
        print("ERROR: missing data from database")
        return 1
        
    kin = boto3.client('kinesis', aws_access_key_id=os.environ.get("ACCESS_KEY"),aws_secret_access_key=os.environ.get("SECRET_KEY"))
    fake = Faker()
    while(True):
        if random.random() < chance: #are we going to add a record this interval
            if(options & mask_t != 0):
                ts.loopers(accounts, fake, kin)
            if(options & mask_ct != 0):
                cs.loopers(accounts, cards, fake, kin) 
            #if(options & 0b0100 != 0):
                #ls.loopers(kin)

        time.sleep(interval)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please specify your options! \
            \n1 for transaction streamer \
            \n2 for card transaction streamer")
        exit()
    if (len (sys.argv) == 4):
        interval = sys.argv[2]
        chance = sys.argv[3]
    else:
        interval = 0.0
        chance = 0.8
    options = int(sys.argv[1])
    if random.random() < chance: #are we going to add a record this interval
            if(options & mask_t != 0):
                print("starting transaction streamer")
            if(options & mask_ct != 0):
                print("starting card transaction streamer")

    stream(options, interval, chance)
    