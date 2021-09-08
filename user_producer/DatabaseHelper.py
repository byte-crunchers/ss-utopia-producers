import json
import traceback

import mysql
import jaydebeapi
from mysql.connector import Error


# !!!!!!IMPORTANT!!!!!!! You must enter the path of a json file on your local machine that contains the database info
# This method connects to the data base
def connect():
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


# def connect_h2():
#     connection = jaydebeapi.connect(
#         "org.h2.Driver",
#         "jdbc:h2:~/test/users",
#         ["meehan", "Wyattdoc12345!"],
#         "C:/Program Files/h2/bin/h2-1.4.199"
#     )
#     curs = connection.cursor()


# This method clears the table of all data and resets the auto increment
def clear_table(table):
    query1 = "SET SQL_SAFE_UPDATES = 0;"
    query2 = "delete from {} where 1 = 1;".format(table)
    query3 = "SET SQL_SAFE_UPDATES = 1;"
    query4 = "ALTER TABLE users AUTO_INCREMENT = 0;"
    connection = connect()
    curs = connection.cursor()
    try:
        curs.execute(query1)
        curs.execute(query2)
        curs.execute(query3)
        curs.execute(query4)
    except Error:
        traceback.print_exc()
        print("There was a problem clearing the user table!")
    connection.commit()
    connection.close()


# This returns the count of all rows in the table
def count_rows(table):
    conn = connect()
    curs = conn.cursor()
    query = "select count(*) from {}".format(table)
    count = None
    try:
        curs.execute(query)
        count = curs.fetchall()[0][0]
    except Error:
        traceback.print_exc(
            print("There was a problem counting the rows")
        )
    conn.close()
    return count


# This method adds a single user to the user table with hardcoded dummy data (for testing purposes)
def add_test_user():
    conn = connect()
    curs = conn.cursor()
    query = "insert into users(username, email, password, first_name, last_name, is_admin) values(%s, %s, %s, %s, " \
            "%s, %s) "
    values = ("Test user", "Test email", "$2a$12$Mgk6lVz7bwGINYAnYHtnXe3e3NqTJ20njH.xWVxKer4OeCWFR4Nnm", "Test fname",
              "Test lname", 1)
    try:
        curs.execute(query, values)
    except Error:
        traceback.print_exc()
        print("There was a problem adding the single test user")
    conn.commit()
    conn.close()
