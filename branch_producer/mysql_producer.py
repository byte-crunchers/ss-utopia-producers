import json

import mysql
from mysql.connector import Error

from branch_producer import generate_branches
from branch_producer import populate_branches


def connect_mysql():
    con_try = None
    try:
        f = open('C:/Users/meeha/OneDrive/Desktop/SmoothStack/Data/dbkey.json', 'r')
        key = json.load(f)
        con_try = mysql.connector.connect(user=key["user"], password=key["password"], host=key["host"],
                                          database=key["database"])
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if con_try.is_connected():
        return con_try
    else:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
        print(Error)


if __name__ == '__main__':
    connect_mysql()
    conn = connect_mysql()
    conn_small = conn
    branches_small = generate_branches(10)
    populate_branches(branches_small, conn, "branches")
    conn_small.close()
