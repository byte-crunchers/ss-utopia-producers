import json
import traceback

import jaydebeapi
import mysql
from mysql.connector import Error
from GenerateUserData import *
from UserProducer import *


# !!!!!!IMPORTANT!!!!!!! You must enter the path of a json file on your local machine that contains the database info
# This method connects to a local MySQL data base
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


# This method connects to a h2 database
def connect_h2():
    con_try = None
    try:
        f = open('C:/Users/meeha/OneDrive/Desktop/SmoothStack/Data/h2_dbkey.json', 'r')
        key = json.load(f)
        con_try = jaydebeapi.connect(
            key["driver"],
            key["url"],
            [key["username"], key["password"]],
            key["jarpath"]
        )
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if con_try is None:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    else:
        return con_try


def clear_table(table, clear_conn):
    clear_query = "DELETE FROM {};".format(table)
    try:
        clear_curs = clear_conn.cursor()
        clear_curs.execute(clear_query)
    except Error:
        traceback.print_exc()
        print("There was a problem clearing the user table!")
    clear_conn.commit()


# This returns the count of all rows in the table
def count_rows(table, count_conn):
    count_curs = count_conn.cursor()
    count_query = "select count(*) from {}".format(table)
    row_count = None
    try:
        count_curs.execute(count_query)
        row_count = count_curs.fetchall()[0][0]
    except Error:
        traceback.print_exc(
            print("There was a problem counting the rows")
        )
    return row_count


# This method adds a single user to the user table with hardcoded dummy data (for testing purposes)
def add_test_user():
    add_conn = connect_mysql()
    add_curs = add_conn.cursor()
    test_query = "insert into users(username, email, password, first_name, last_name, is_admin) values(%s, %s, %s, " \
                 "%s, %s, %s) "
    values = ("Test user", "Test email", "$2a$12$Mgk6lVz7bwGINYAnYHtnXe3e3NqTJ20njH.xWVxKer4OeCWFR4Nnm", "Test fname",
              "Test lname", 1)
    try:
        add_curs.execute(test_query, values)
    except Error:
        traceback.print_exc()
        print("There was a problem adding the single test user")
    add_conn.commit()
    add_conn.close()


# This method adds a single user to the user table on with hardcoded dummy data (for testing purposes)
def add_test_user_h2():
    add_h2_conn = connect_h2()
    add_h2_curs = add_h2_conn.cursor()
    add_h2_query = "INSERT INTO bytecruchers.users (USERNAME, EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, IS_ADMIN) " \
                   "VALUES ('Test Username', 'Test Email', " \
                   "'$2a$12$Mgk6lVz7bwGINYAnYHtnXe3e3NqTJ20njH.xWVxKer4OeCWFR4Nnm', 'Test First', 'Test Last', 0); "
    try:
        add_h2_curs.execute(add_h2_query)
    except Error:
        traceback.print_exc()
        print("There was a problem adding the single test user")
    add_h2_conn.commit()
    add_h2_conn.close()

