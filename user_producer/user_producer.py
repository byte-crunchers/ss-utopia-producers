import random
import traceback

import bcrypt
import jaydebeapi
from faker import Faker
from pyzipcode import ZipCodeDatabase
from random_username.generate import generate_username

fake = Faker()
zip_database = ZipCodeDatabase()
valid_zips = []
for x in zip_database:
    valid_zips.append(x)


class User:
    def __init__(self, user, email, password, f_name, l_name, is_admin, ssn, active, confirmed, phone, dob,
                 street_address, city, state, zip_code):
        self.user = user
        self.email = email
        self.password = password
        self.f_name = f_name
        self.l_name = l_name
        self.is_admin = is_admin
        self.ssn = ssn
        self.active = active
        self.confirmed = confirmed
        self.phone = phone
        self.dob = dob
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def print_user(self):
        print(
            self.user + ", " + self.email + ", " + self.password + ", " + self.f_name + ", " + self.l_name + ", " +
            str(self.is_admin) + ", " + self.ssn + ", " + str(self.active) + ", " + str(self.confirmed) + ", "
            + str(self.phone) + ", " + str(self.dob) + ", " + self.street_address + ", " + self.city + ", "
            + self.state + ", " + self.zip_code)


def populate_users(user_data, pop_conn):
    duplicate_count = 0
    dd_count = 0
    curs = pop_conn.cursor()
    query = "INSERT INTO users(username, email, password, first_name, last_name, is_admin, ssn, active, " \
            "confirmed, phone, dob, street_address, city, state, zip) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
            "?, ?, ?) "
    for user in user_data:
        vals = (user.user, user.email, user.password, user.f_name, user.l_name, user.is_admin, user.ssn, user.active,
                user.confirmed, user.phone, str(user.dob), user.street_address, user.city, user.state, user.zip_code)
        try:
            curs.execute(query, vals)
        except jaydebeapi.DatabaseError:  # Check for Duplicates
            traceback.print_exc()
            duplicate_count += 1
            # Find a unique username and email that is not in the database
            while True:
                query = "INSERT INTO users(username, email, password, first_name, last_name, is_admin, ssn, active, " \
                        "confirmed, phone, dob, street_address, city, state, zip) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, " \
                        "?, ?, ?, ?, ?, ?) "
                try:
                    vals = (get_username(), get_email(user.f_name, user.l_name), user.password, user.f_name,
                            user.l_name, user.is_admin, get_ssn(), user.active, user.confirmed, user.phone,
                            str(user.dob), user.street_address, user.city, user.state, user.zip_code)
                    curs.execute(query, vals)
                    break
                except jaydebeapi.DatabaseError:
                    dd_count += 1
                    continue
        except Exception:
            print("There was a problem writing to the database. ")
            traceback.print_exc()
    print("\n{} duplicate usernames or emails were generated and replaced!".format(duplicate_count))
    print("{} double duplicate usernames or emails were generated and replaced!".format(dd_count))


def get_user_data(num_of_users):
    users = []
    for _ in range(num_of_users):
        f_name = fake.first_name()
        l_name = fake.last_name()
        state = get_zip_and_state()[1]
        zip_code = get_zip_and_state()[0]
        users.append(
            User(get_username(), get_email(f_name, l_name), get_pass(), f_name, l_name, get_is_admin(), get_ssn(),
                 get_active(), get_confirmed(), int(fake.numerify('##########')),
                 fake.date_between(start_date='-100y', end_date='-18y'), get_street_address(), fake.city(),
                 state, zip_code)
        )
    return users


def get_username():
    while True:
        username = generate_username(1)[0]
        if len(username) <= 16:
            return username
        else:
            continue


# This method generates a random email based on the first and last name
def get_email(f_name, l_name):
    email = None
    suffix = fake.email().split("@", 1)[1]
    chance = random.randint(0, 8)
    if chance == 0:
        email = f_name[0].lower() + "." + l_name[0:].lower()
    elif chance == 1:
        email = f_name.lower() + "." + l_name.lower()
    elif chance == 2:
        email = f_name.lower() + l_name.lower()
    elif chance == 3:
        email = l_name.lower() + "." + f_name.lower()
    elif chance == 4:
        email = l_name.lower() + f_name.lower()
    elif chance == 5:
        email = f_name.lower() + l_name[0].lower()
    elif chance == 6:
        email = l_name.lower()[0] + "." + f_name.lower()
    else:
        email = l_name.lower()[0] + f_name.lower()
    email += str(random.randint(0, 10000))
    email += "@" + suffix
    return email


def get_pass():
    password_length = random.randint(12, 15)
    possible_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!#$%&'" \
                          "()*+,-./:;<=>?@[\]^_`{|}~"
    password = "".join([random.choice(possible_characters) for _ in range(password_length)])
    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10))
    return hashed


def get_is_admin():
    chance = random.randint(0, 10)
    if chance >= 2:
        return False
    else:
        return True


def get_active():
    if random.random() < 0.1:
        return False
    return True


def get_confirmed():
    if random.random() < 0.1:
        return False
    return True


def get_street_address():
    return fake.building_number() + " " + fake.street_name() + "\n"


def get_zip_and_state():
    choice = random.choice(valid_zips)
    zip_code = zip_database[choice]
    state = zip_code.state
    return choice, state


def get_ssn():
    ssn = fake.ssn().replace('-', "").strip()
    return ssn


def execute_scripts_from_file(filename, conn):
    # Open and read the file as a single buffer
    sql_file = None
    try:
        fd = open(filename, 'r')
        sql_file = fd.read()
        fd.close()
    except IOError:
        traceback.print_exc()
    # all SQL commands (split on ';')
    sql_commands = sql_file.split(';')
    # Execute every command from the input file
    curs = conn.cursor()
    for command in sql_commands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            curs.execute(command)
        except (jaydebeapi.OperationalError, jaydebeapi.DatabaseError, Exception):
            print("\nCould not execute: " + command + "\n")
