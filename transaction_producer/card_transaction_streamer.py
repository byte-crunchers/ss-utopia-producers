import transaction_producer.transaction_producer as tp
import time
import json
import boto3
import random
from faker import Faker

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
    

def stream(interval: float = 5, chance: float = 1) -> None:
    conn = tp.connect()
    accounts = tp.get_accounts(conn)
    cards = tp.get_cards(conn)
    if (len(accounts) == 0 or len(cards) == 0):
        print("ERROR: missing data from database")
        return 1
    f = open('awskey.json', 'r')
    key = json.load(f)      
    kin = boto3.client('kinesis', aws_access_key_id=key['access_key'], aws_secret_access_key=key['secret_key'])
    fake = Faker()
    while(True):
        if random.random() < chance: #are we going to add a record this interval
            loopers(accounts, cards, fake, kin)
        time.sleep(interval)

if __name__ == "__main__":
    stream(0.0, 0.8)
    