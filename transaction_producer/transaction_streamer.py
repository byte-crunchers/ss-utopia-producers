import transaction_producer as tp
import time
import json
import boto3
import random
from faker import Faker

def loopers(accounts: tuple, fake: Faker, kin ) -> None:
    accounts_sample = random.sample(accounts, 2) #use so that we can have two random, unique accounts
    trans = tp.Transaction(fake, accounts_sample[0][0], accounts_sample[1][0])
    resp = kin.put_record(StreamName='byte-henry', Data=json.dumps(trans.__dict__, default=str), PartitionKey='trans key')
    #print (resp)

def stream(interval: float = 5, chance: float = 1) -> None:
    accounts = tp.get_accounts(tp.connect())
    if (len(accounts) == 0):
        print("ERROR: missing accounts from database")
        return 1
    f = open('awskey.json', 'r')
    key = json.load(f)      
    kin = boto3.client('kinesis', aws_access_key_id=key['access_key'], aws_secret_access_key=key['secret_key'])
    fake = Faker()
    while(True):
        if random.random() < chance: #are we going to add a record this interval
            loopers(accounts, fake, kin)
        time.sleep(interval)

if __name__ == "__main__":
    stream(0.5, 0.25)
    