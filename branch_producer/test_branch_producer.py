import os

import jaydebeapi
import pytest
from jaydebeapi import Error

from branch_producer import generate_branches, populate_branches, clear_table, count_rows, execute_scripts_from_file, \
    Branch

table = "branches"
script_dir = os.path.dirname(__file__)
schema_path = os.path.join(script_dir, "../schema_h2.sql")


# This method connects to a h2 database
@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con_try = None
    try:
        con_try = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL;DATABASE_TO_UPPER"
                                                      "=FALSE;", ["sa", ""], os.environ.get("H2"))
        con_try.jconn.setAutoCommit(False)
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if con_try is None:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    else:
        return con_try


# Test connection and create the schema
def test_create_schema(connect_h2):
    execute_scripts_from_file(schema_path, connect_h2)
    assert connect_h2
    connect_h2.rollback()


def test_small(connect_h2):
    branches_small = generate_branches(10)
    clear_table(connect_h2)
    populate_branches(branches_small, connect_h2)
    count_small = count_rows(table, connect_h2)
    assert (10 == count_small)
    clear_table(connect_h2)
    count_small = count_rows(table, connect_h2)
    assert (0 == count_small)
    connect_h2.rollback()


def test_large(connect_h2):
    branches_large = generate_branches(1000)
    clear_table(connect_h2)
    populate_branches(branches_large, connect_h2)
    count_large = count_rows(table, connect_h2)
    assert (1000 == count_large)
    clear_table(connect_h2)
    count_large = count_rows(table, connect_h2)
    assert (0 == count_large)
    connect_h2.rollback()


def test_stress(connect_h2):
    branches_large = generate_branches(10000)
    clear_table(connect_h2)
    populate_branches(branches_large, connect_h2)
    count_stress = count_rows(table, connect_h2)
    assert (10000 == count_stress)
    clear_table(connect_h2)
    count_stress = count_rows(table, connect_h2)
    assert (0 == count_stress)
    connect_h2.rollback()


def test_duplicate(connect_h2):
    clear_table(connect_h2)
    branch_data_one = [Branch("Test Address", "Test City", "CA", "45056")]
    branch_data_two = [Branch("Test Address", "Test City", "CA", "45056")]
    populate_branches(branch_data_one, connect_h2)
    populate_branches(branch_data_two, connect_h2)
    count_dup = count_rows(table, connect_h2)
    assert (2 == count_dup)
    clear_table(connect_h2)
    count_dup = count_rows(table, connect_h2)
    assert (0 == count_dup)
    connect_h2.rollback()


if __name__ == '__main__':
    pytest.main()
