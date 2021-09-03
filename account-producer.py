import mysql
from mysql.connector import Error

def connect():
    con_try = None
    try:
        con_try = mysql.connector.connect(user='root', password='root', #Enter password here
                                          host='localhost',
                                          database='bytecrunchers')
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if con_try.is_connected():
        return con_try
    else:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
        print(Error)