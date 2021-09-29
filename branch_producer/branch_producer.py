import random
import traceback

import jaydebeapi
import mysql
from faker import Faker
from mysql.connector import Error
from pyzipcode import ZipCodeDatabase

fake = Faker()
zip_database = ZipCodeDatabase()
valid_zips = []
for x in zip_database:
    valid_zips.append(x)
choice = random.choice(valid_zips)


class Branch:
    def __init__(self, street_address, city, state, zip):
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip = zip
    def print_branch(self):
        print(self.street_address, self.city, self.state, self.zip)


def get_street_address():
    return fake.building_number() + " " + fake.street_name() + "\n"


def get_city():
    return fake.city()


def get_zip_and_state():
    zip_code = zip_database[choice]
    state = zip_code.state
    return zip_code.zip, state


def generate_branches(num_of_branches):
    branches = []
    for _ in range(0, num_of_branches):
        state = get_zip_and_state()[1]
        zip = get_zip_and_state()[0]
        branches.append(Branch(get_street_address(), get_city(), state, zip))
    return branches


def populate_branches(branch_data, pop_conn):
    duplicate_count = 0
    dd_count = 0
    curs = pop_conn.cursor()
    query = "INSERT INTO branches (street_address, city, state, zip) VALUES (?, ?, ?, ?)"
    for branch in branch_data:
        try:
            vals = (branch.street_address, branch.city, branch.state, branch.zip)
            curs.execute(query)
        except (mysql.connector.errors.IntegrityError, jaydebeapi.DatabaseError):  # Check for Duplicates
            duplicate_count += 1
            while True:
                try:
                    curs.execute(query, vals)
                    break
                except (mysql.connector.errors.IntegrityError, jaydebeapi.DatabaseError):
                    dd_count += 1
                    continue
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()
    print("\n{} duplicate addresses were generated and replaced!".format(duplicate_count))
    print("{} double duplicate addresses were generated and replaced!".format(dd_count))


if __name__ == '__main__':
    branches = generate_branches(10)
    for b in branches:
        b.print_branch()
