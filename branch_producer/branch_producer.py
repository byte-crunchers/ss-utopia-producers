import random
import traceback

import jaydebeapi
from faker import Faker
from jaydebeapi import Error
from pyzipcode import ZipCodeDatabase

fake = Faker()
zip_database = ZipCodeDatabase()
valid_zips = []
for x in zip_database:
    valid_zips.append(x)


class Branch:
    def __init__(self, street_address, city, state, zip_code):
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip = zip_code

    def print_branch(self):
        print(self.street_address, self.city, self.state, self.zip)


def get_street_address():
    return fake.building_number() + " " + fake.street_name() + "\n"


def get_city():
    return fake.city()


def get_zip_and_state():
    choice = random.choice(valid_zips)
    zip_code = zip_database[choice]
    state = zip_code.state
    return choice, state


def generate_branches(num_of_branches):
    ret_branches = []
    for _ in range(0, num_of_branches):
        state = get_zip_and_state()[1]
        zip_code = get_zip_and_state()[0]
        ret_branches.append(Branch(get_street_address(), get_city(), state, zip_code))
    return ret_branches


def populate_branches(branch_data, pop_conn):
    duplicate_count = 0
    dd_count = 0
    query = None
    curs = pop_conn.cursor()
    for branch in branch_data:
        try:
            query = "INSERT INTO branches(street_address, city, state, zip) VALUES(?, ?, ?, ?) "
            vals = (branch.street_address, branch.city, branch.state, branch.zip)
            curs.execute(query, vals)
        except jaydebeapi.DatabaseError:  # Check for Duplicates
            duplicate_count += 1
            while True:
                try:
                    vals = (get_street_address(), get_city(), branch.state, branch.zip)
                    curs.execute(query, vals)
                    break
                except jaydebeapi.DatabaseError:
                    dd_count += 1
                    continue
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()
    print("\n{} duplicate addresses were generated and replaced!".format(duplicate_count))
    print("{} double duplicate addresses were generated and replaced!".format(dd_count))
