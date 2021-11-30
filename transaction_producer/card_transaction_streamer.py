import transaction_producer.transaction_producer as tp
import os
import time
import json
import boto3
import random
from faker import Faker
from botocore.config import Config

access_key = os.environ.get("ACCESS_KEY")
secret_key = os.environ.get("SECRET_KEY")

my_config = Config(
    region_name='us-east-1'
)


def loopers(accounts: tuple, cards: tuple, fake: Faker, kin, kaf) -> None:
    account = random.choice(accounts)
    if random.random() < 0.95: #valid credentials
        card = random.choice(cards)
    elif random.random() < 0.80: #valid card number, invalid cvc and pin
        card = (random.choice(cards)[0], random.randint(0, 999), random.randint(0, 999), random.randint(0, 999))
    else: #invalid card number
        card = (random.randint(0, 9999999999999999), random.randint(0, 999), random.randint(0, 999), random.randint(0, 999))
    
    trans = tp.Card_Transaction(fake, card[0], account[0], pin=card[1])
    if random.random() < 0.25:  # 1/4 chance of a mag-swipe, 1/4 its amazon, 2/4 online/phone transaction from a reputable store
        trans.cvc1 = card[2]
    elif random.random() < 0.33:
        pass  # amazon does not use cvc because they don't care about the consumer
    else:
        trans.cvc2 = card[3]

    trans.type = 'card_transaction' #for the consumer to know what type of message it is
    #print(json.dumps(trans.__dict__, default=str))
    if kin: #If we're using kinesis this will be non-null
        kin.put_record(StreamName='byte-henry', Data=json.dumps(trans.__dict__, default=str), PartitionKey='card trans key')
    elif kaf: #Streaming to Kafka on Axure
        kaf.send('quickstart-events', value=trans)


def stream(interval: float = 5, chance: float = 1) -> None:
    conn = tp.connect()
    accounts = tp.get_accounts(conn)
    cards = tp.get_cards(conn)
    if len(accounts) == 0 or len(cards) == 0:
        print("ERROR: missing data from database")
        return 1
    kin = boto3.client('kinesis', config=my_config, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    fake = Faker()
    while True:
        if random.random() < chance:  # are we going to add a record this interval
            loopers(accounts, cards, fake, kin)
        time.sleep(interval)


if __name__ == "__main__":
    stream(0.0, 0.8)