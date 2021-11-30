import transaction_producer as tp
import time
import os
import sys
import boto3
import random
import threading
import json

import transaction_producer.transaction_streamer as ts
import transaction_producer.card_transaction_streamer as cs
import transaction_producer.transaction_producer as tp
from kafka import KafkaProducer

from faker import Faker

mask_t = 1
mask_ct = 2
mask_lp = 4
mask_stock = 8

   

def stream(options: int = 0b1111, interval: float = 5, chance: float = 1, kafka_ip: str = None) -> None:
    conn = tp.connect()
    accounts = tp.get_accounts(conn)
    cards = tp.get_cards(conn)
    if (len(accounts) == 0 or len(cards) == 0):
        print("ERROR: missing data from database")
        return 1
    if(kafka_ip):
        kin = None
        kaf = KafkaProducer(bootstrap_servers=[kafka_ip], value_serializer = lambda x: json.dumps(x.__dict__, default=str).encode('utf-8'))
    else:
        kaf = None
        kin = boto3.client('kinesis', aws_access_key_id=os.environ.get("ACCESS_KEY"),aws_secret_access_key=os.environ.get("SECRET_KEY"))
    fake = Faker()
    while(True):
        if random.random() < chance: #are we going to add a record this interval
            if(options & mask_t != 0):
                ts.loopers(accounts, fake, kin, kaf)
            if(options & mask_ct != 0):
                cs.loopers(accounts, cards, fake, kin, kaf) 
            #if(options & 0b0100 != 0):
                #ls.loopers(kin)

        time.sleep(interval)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please specify your options! \
             \n--producers |-p     1 for transaction streamer \
             \n                    2 for card transaction streamer \
             \n--threads   |-t     Indecate the number of threads/db connections \
             \n--kafka     |-k     Stream to kafka instead of azure. Must specify address")
        exit()
    threadCount = 1
    options = 3 #transactions and card transactions
    kafka_ip = None
    i = 1
    while i < len(sys.argv): #options select loop
        if sys.argv[i] == "--producers" or sys.argv[i] == "-p":
            try:
                options = int(sys.argv[i+1])
                i=i+2 #only increment after after we've made a successful cast
            except:
                print ("Invalid argument to " + sys.argv[i])
                break

        elif sys.argv[i] == "--threads" or sys.argv[i] == "-t":
            try:
                threadCount = int(sys.argv[i+1])
                i=i+2 #only increment after after we've made a successful cast
            except:
                print ("Invalid argument to " + sys.argv[i])
                break

        elif sys.argv[i] == "--kafka" or sys.argv[i] == "-k":
            try:
                kafka_ip = sys.argv[i+1]
                i=i+2 #only increment after after we've made sure we have an ip
            except:
                print ("Invalid argument to " + sys.argv[i])
                break
        else: 
            print("Invalid command: " + sys.argv[i])
            break
    
    conn = tp.connect() #I have to do this so jaydebeapi starts the JVM ahead of time
    interval = 0.0
    chance = 0.8
    if(options & mask_t != 0):
        print("starting transaction streamer")
    if(options & mask_ct != 0):
        print("starting card transaction streamer")
    threads = []

    for i in range(0, threadCount):
        t = threading.Thread(target=stream, args=(options, interval, chance, kafka_ip))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    conn.close()
        
    