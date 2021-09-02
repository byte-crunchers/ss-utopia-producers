import traceback

import mysql
from mysql.connector import Error
from time import process_time

from GenerateUserData import get_user_data
from GenerateUserData import generate_username


def connect():
    con_try = None
    try:
        con_try = mysql.connector.connect(user='root', password='***************', #Enter password here
                                          host='localhost',
                                          database='bytecrunchers')
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if con_try.is_connected():
        return con_try
    else:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
        print(Error)


def populate(connection, user_data):
    query = "insert into users(username, email, password, first_name, last_name, is_admin) values(%s, %s, %s, %s, %s," \
            "%s) "
    curs = connection.cursor()
    for user in user_data:
        vals = (user.user, user.email, user.password, user.f_name, user.l_name, user.is_admin)
        try:
            curs.execute(query, vals)
        except mysql.connector.errors.IntegrityError:
            print("Duplicate entry found, skipping addition and attempting to get new username...")
            # Find a unique username that is not in the database
            while True:
                try:
                    vals = (generate_username()[0], user.email, user.password, user.f_name, user.l_name, user.is_admin)
                    curs.execute(query, vals)
                    print("Replacement username found successfully")
                    break
                except mysql.connector.errors.IntegrityError:
                    print("The Generator returned another duplicate, WHAT ARE THE CHANCES!!!")
                    continue
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()

    connection.commit()


if __name__ == '__main__':
    time_start = process_time()
    users = get_user_data(10000)
    populate(connect(), users)
    time_stop = process_time()
    print("The process took {:0.0f} seconds".format(time_stop-time_start))