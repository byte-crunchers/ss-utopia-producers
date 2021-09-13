import traceback

import jaydebeapi
import mysql
from mysql.connector import Error

from database_helper import count_rows
from generate_user_data import generate_username, get_user_data
from generate_user_data import get_email


def populate_users(user_data, pop_conn, pop_table):
    duplicate_count = 0
    dd_count = 0
    curs = pop_conn.cursor()
    for user in user_data:
        query = "INSERT INTO {}(username, email, password, first_name, last_name, is_admin) VALUES('{}', '{}', '{}', " \
                "'{}', '{}', {}) ".format(pop_table, user.user, user.email, user.password, user.f_name, user.l_name,
                                          user.is_admin)
        try:
            curs.execute(query)
        except (mysql.connector.errors.IntegrityError, jaydebeapi.DatabaseError):  # Check for Duplicates
            duplicate_count += 1
            # Find a unique username and email that is not in the database
            while True:
                try:
                    query = "INSERT INTO {}(username, email, password, first_name, last_name, is_admin) VALUES('{}', " \
                            "'{}', '{}', '{}', '{}', {}) ".format(pop_table, generate_username()[0], get_email(
                        user.f_name, user.l_name), user.password, user.f_name, user.l_name, user.is_admin)
                    curs.execute(query)
                    break
                except (mysql.connector.errors.IntegrityError, jaydebeapi.DatabaseError):
                    dd_count += 1
                    continue
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()
    print("\n{} duplicate usernames or emails were generated and replaced!".format(duplicate_count))
    print("{} double duplicate usernames or emails were generated and replaced!".format(dd_count))
    pop_conn.commit()

