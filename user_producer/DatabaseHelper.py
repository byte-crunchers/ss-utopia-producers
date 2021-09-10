import json
import traceback

import jaydebeapi
import mysql
from mysql.connector import Error
from GenerateUserData import *
from UserProducer import *


# !!!!!!IMPORTANT!!!!!!! You must enter the path of a json file on your local machine that contains the database info
# This method connects to the data base
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


# This method clears the table of all data and resets the auto increment
def clear_table(table):
    query1 = "SET SQL_SAFE_UPDATES = 0;"
    query2 = "DELETE FROM {};".format(table)
    query3 = "SET SQL_SAFE_UPDATES = 1;"
    query4 = "ALTER TABLE users AUTO_INCREMENT = 0;"
    clear_conn = connect_mysql()
    try:
        clear_curs = clear_conn.cursor()
        clear_curs.execute(query1)
        clear_curs.execute(query2)
        clear_curs.execute(query3)
        clear_curs.execute(query4)
    except Error:
        traceback.print_exc()
        print("There was a problem clearing the user table!")
    clear_conn.commit()
    clear_conn.close()


def clear_table_h2(table):
    clear_h2_conn = connect_h2()
    clear_h2_query = "DELETE FROM {};".format(table)
    try:
        clear_h2_curs = clear_h2_conn.cursor()
        clear_h2_curs.execute(clear_h2_query)
    except Error:
        traceback.print_exc()
        print("There was a problem clearing the user table!")
    clear_h2_conn.commit()
    clear_h2_conn.close()


# This returns the count of all rows in the table
def count_rows(table):
    count_conn = connect_mysql()
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
    count_conn.close()
    return row_count


def count_rows_h2(table):
    count_h2_conn = connect_h2()
    count_h2_curs = count_h2_conn.cursor()
    count_h2_query = "SELECT count(*) FROM {};".format(table)
    h2_row_count = None
    try:
        count_h2_curs.execute(count_h2_query)
        h2_row_count = count_h2_curs.fetchall()[0][0]
    except Error:
        traceback.print_exc(
            print("There was a problem counting the rows")
        )
    count_h2_conn.close()
    return h2_row_count


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


if __name__ == '__main__':
    conn = connect_h2()
    h2_table = "BYTECRUCHERS.USERS"
    users = get_user_data(10)
    populate_users(users, conn, h2_table)
    count = count_rows_h2(h2_table)
    print(count)
