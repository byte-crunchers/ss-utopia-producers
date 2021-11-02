import transaction_producer.transaction_producer as tp
import time
import json
import os
import random
import time

import boto3
from botocore.config import Config
from faker import Faker

access_key = os.environ.get("ACCESS_KEY")
secret_key = os.environ.get("SECRET_KEY")

my_config = Config(
    region_name='us-east-1'
)


def loopers(accounts: tuple, fake: Faker, kin) -> None:
    accounts_sample = random.sample(accounts, 2)  # use so that we can have two random, unique accounts
    trans = tp.Transaction(fake, accounts_sample[0][0], accounts_sample[1][0])
    trans.type = 'transaction' #for the consumer to know what type of message it is
    #print(json.dumps(trans.__dict__, default=str))
    kin.put_record(StreamName='byte-henry', Data=json.dumps(trans.__dict__, default=str), PartitionKey='trans key')


def stream(interval: float = 5, chance: float = 1) -> None:
    accounts = tp.get_accounts(tp.connect())
    if len(accounts) == 0:
        print("ERROR: missing accounts from database")
        return 1
    kin = boto3.client('kinesis', config=my_config, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    fake = Faker()
    while True:
        if random.random() < chance:  # are we going to add a record this interval
            loopers(accounts, fake, kin)
        time.sleep(interval)


if __name__ == "__main__":
    stream(0.4, 0.2)
