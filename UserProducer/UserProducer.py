from mysql.connector import Error

from DatabaseHelper import *
from GenerateUserData import generate_username


def populate_users(user_data):
    connection = connect()
    duplicate_count = 0
    dd_count = 0
    query = "insert into users(username, email, password, first_name, last_name, is_admin) values(%s, %s, %s, %s, %s," \
            "%s) "
    curs = connection.cursor()
    for user in user_data:
        values = (user.user, user.email, user.password, user.f_name, user.l_name, user.is_admin)
        try:
            curs.execute(query, values)
        except mysql.connector.errors.IntegrityError:
            duplicate_count += 1
            # Find a unique username that is not in the database
            while True:
                try:
                    values = (
                        generate_username()[0], user.email, user.password, user.f_name, user.l_name, user.is_admin)
                    curs.execute(query, values)
                    break
                except mysql.connector.errors.IntegrityError:
                    dd_count += 1
                    continue
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()
    print("\n{} duplicate usernames were generated and replaced!".format(duplicate_count))
    print("{} double duplicate usernames were generated and replaced!".format(dd_count))
    connection.commit()
    connection.close()
