import traceback

import mysql
from mysql.connector import Error


# !!!!!!IMPORTANT!!!!!!! You must enter the path of a txt file on your local machine that contains the password
# of the database, You must also enter accurate data for root, host, and database
# This method connects to the data base
def connect():
    password = None
    try:
        file = open("C:/Users/meeha/OneDrive/Desktop/SmoothStack/Data/pass.txt", "r")
        password = file.read()
        file.close()
    except IOError:
        traceback.print_exc()
        print("There was a problem reading pass.txt, please ensure the path is correct!")
    con_try = None
    try:
        con_try = mysql.connector.connect(user='root', password=password,  # Enter password here
                                          host='localhost',
                                          database='bytecrunchers')
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if con_try.is_connected():
        return con_try
    else:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
        print(Error)


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
    values = ("Test user", "Test email", "Test pass", "Test fname", "Test lname", 1)
    try:
        curs.execute(query, values)
    except Error:
        traceback.print_exc()
        print("There was a problem adding the single test user")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    connect()
