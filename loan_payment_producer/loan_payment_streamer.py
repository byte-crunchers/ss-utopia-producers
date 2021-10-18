import json
import os
import random
import time

import boto3
from botocore.config import Config
import loan_payment_producer as lpp

access_key = os.environ.get("ACCESS_KEY")
secret_key = os.environ.get("SECRET_KEY")

my_config = Config(
    region_name='us-east-1'
)


def loopers(kin) -> None:
    loan_id = random.sample(lpp.get_table_id(lpp.connect(), "loans"), 1)[0][0]  # Get one random loan_id from db
    # Get one random account_id from db
    account_id = random.sample(lpp.get_table_id(lpp.connect(), "accounts"), 1)[0][0]
    trans = lpp.Payment(loan_id, account_id)
    trans.type = 'loan_payment'  # for the consumer to know what type of message it is
    print(json.dumps(trans.__dict__, default=str))
    kin.put_record(StreamName='byte-henry', Data=json.dumps(trans.__dict__, default=str), PartitionKey='trans key')


def stream(interval: float = 5, chance: float = 1) -> None:
    kin = boto3.client('kinesis', config=my_config, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    while True:
        if random.random() < chance:  # are we going to add a record this interval
            loopers(kin)
        time.sleep(interval)


if __name__ == "__main__":
    stream(0.4, 0.2)
