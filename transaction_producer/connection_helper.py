import jaydebeapi
import json
from jaydebeapi import Error

def connect():
    con_try = None
    try:
        f = open('../dbkey.json', 'r')
        key = json.load(f)        
        con_try = jaydebeapi.connect(key["driver"], key["location"], key["login"], key["jar"] )
        con_try.jconn.setAutoCommit(False)
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    return con_try