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


class Branch:
    def __init__(self, location):
        self.location = location


def get_address():
    choice = random.choice(valid_zips)
    zip_code = zip_database[choice]
    state = zip_code.state
    return fake.building_number() + " " + fake.street_name() + ",\n" + fake.city() + ", " + state + " " + choice


def generate_branches(num_of_branches):
    branches = []
    for x in range(num_of_branches):
        location = get_address()
        branches.append(Branch(location))
    return branches


def populate_branches(branch_data, pop_conn, pop_table):
    duplicate_count = 0
    dd_count = 0
    curs = pop_conn.cursor()
    for branch in branch_data:
        query = "INSERT INTO {}(location) VALUES ('{}')".format(pop_table, branch.location)
        try:
            curs.execute(query)
        except (mysql.connector.errors.IntegrityError, jaydebeapi.DatabaseError):  # Check for Duplicates
            duplicate_count += 1
            while True:
                try:
                    query = "INSERT INTO {}(location) VALUES ('{}')".format(pop_table, get_address())
                    curs.execute(query)
                    break
                except (mysql.connector.errors.IntegrityError, jaydebeapi.DatabaseError):
                    dd_count += 1
                    continue
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()
    print("\n{} duplicate addresses were generated and replaced!".format(duplicate_count))
    print("{} double duplicate addresses were generated and replaced!".format(dd_count))
    pop_conn.commit()


if __name__ == '__main__':
    get_address()
