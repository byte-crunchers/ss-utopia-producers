import traceback
from time import process_time

from mysql.connector import Error

from DatabaseHelper import *
from GenerateUserData import generate_username
from GenerateUserData import get_user_data


def populate(user_data):
    connection = connect()
    query = "insert into users(username, email, password, first_name, last_name, is_admin) values(%s, %s, %s, %s, %s," \
            "%s) "
    curs = connection.cursor()
    for user in user_data:
        values = (user.user, user.email, user.password, user.f_name, user.l_name, user.is_admin)
        try:
            curs.execute(query, values)
        except mysql.connector.errors.IntegrityError:
            print("Duplicate entry found, skipping addition and attempting to get new username...")
            # Find a unique username that is not in the database
            while True:
                try:
                    values = (
                        generate_username()[0], user.email, user.password, user.f_name, user.l_name, user.is_admin)
                    curs.execute(query, values)
                    print("Replacement username found successfully, data inserted")
                    break
                except mysql.connector.errors.IntegrityError:
                    print("The Generator returned another duplicate, WHAT ARE THE CHANCES!!!")
                    continue
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()

    connection.commit()
    connection.close()


if __name__ == '__main__':
    time_start = process_time()
    users = get_user_data(100)
    populate(users)
    time_stop = process_time()
    print("The process took about {:0.02f} seconds".format(time_stop - time_start))
