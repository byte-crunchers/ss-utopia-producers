#combines functions

import random
import traceback

import jaydebeapi
from jaydebeapi import Error
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
    for _ in range(num_of_branches):
        location = get_address()
        branches.append(Branch(location))
    return branches


def populate_branches(branch_data, pop_conn):
    duplicate_count = 0
    dd_count = 0
    curs = pop_conn.cursor()
    for branch in branch_data:
        query = "INSERT INTO branches(location) VALUES ('{}')".format(branch.location)
        try:
            curs.execute(query)
        except (jaydebeapi.DatabaseError):  # Check for Duplicates
            duplicate_count += 1
            while True:
                try:
                    query = "INSERT INTO branches(location) VALUES ('{}')".format(get_address())
                    curs.execute(query)
                    break
                except (jaydebeapi.DatabaseError):
                    dd_count += 1
                    continue
        except Error:
            print("There was a problem writing to the database. ")
            traceback.print_exc()
    print("\n{} duplicate addresses were generated and replaced!".format(duplicate_count))
    print("{} double duplicate addresses were generated and replaced!".format(dd_count))




def clear_table(clear_conn):
    queries = []
    h2_query = "DELETE FROM branches;"
    queries.append(h2_query)
    try:
        clear_curs = clear_conn.cursor()
        for q in queries:
            clear_curs.execute(q)
    except Error:
        traceback.print_exc()
        print("There was a problem clearing the user table!")
    


# This returns the count of all rows in the table
def count_rows(count_conn):
    count_curs = count_conn.cursor()
    count_query = "select count(*) from branches;"
    row_count = None
    try:
        count_curs.execute(count_query)
        row_count = count_curs.fetchall()[0][0]
    except Error:
        traceback.print_exc(
            print("There was a problem counting the rows")
        )
    return row_count


def execute_scripts_from_file(filename, conn):
    # Open and read the file as a single buffer
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
            traceback.print_exc()
    