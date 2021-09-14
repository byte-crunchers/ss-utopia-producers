import json
import os

import jaydebeapi
import pytest
from jaydebeapi import Error

from branch_producer import generate_branches
from branch_producer import populate_branches
from database_helper import clear_table, count_rows, execute_scripts_from_file

table = "BYTECRUNCHERS.BRANCHES"
script_dir = os.path.dirname(__file__)


# This method connects to a h2 database
@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con_try = None
    try:
        f = open('C:/Users/meeha/OneDrive/Desktop/SmoothStack/Data/h2_dbkey.json', 'r')
        key = json.load(f)
        con_try = jaydebeapi.connect(
            key["driver"],
            key["url"],
            [key["username"], key["password"]],
            key["jarpath"]
        )
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if con_try is None:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    else:
        return con_try


def test_drop_schema(connect_h2):
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2DropUsers.sql"), connect_h2)
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2DropBranches.sql"), connect_h2)
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2DropSchema.sql"), connect_h2)
    assert connect_h2
    assert isinstance(connect_h2, jaydebeapi.Connection)


def test_create_schema(connect_h2):
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2CreateSchema.sql"),
                              connect_h2)
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2CreateUsers.sql"),
                              connect_h2)
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2CreateBranches.sql"),
                              connect_h2)


def test_count_clear(connect_h2):
    clear_table(table, connect_h2)
    count_test = count_rows(table, connect_h2)
    assert (0, count_test)
    branches_count = generate_branches(10)
    populate_branches(branches_count, connect_h2, table)
    count_test = count_rows(table, connect_h2)
    assert (10, count_test)
    clear_table(table, connect_h2)
    count_test = count_rows(table, connect_h2)
    assert (0, count_test)


def test_small(connect_h2):
    branches_small = generate_branches(10)
    clear_table(table, connect_h2)
    populate_branches(branches_small, connect_h2, table)
    count_small = count_rows(table, connect_h2)
    assert (10, count_small)
    clear_table(table, connect_h2)
    count_small = count_rows(table, connect_h2)
    assert (0, count_small)


def test_large(connect_h2):
    branches_large = generate_branches(1000)
    clear_table(table, connect_h2)
    populate_branches(branches_large, connect_h2, table)
    count_large = count_rows(table, connect_h2)
    assert (1000, count_large)
    clear_table(table, connect_h2)
    count_large = count_rows(table, connect_h2)
    assert (0, count_large)


def test_stress(connect_h2):
    branches_stress = generate_branches(500000)
    clear_table(table, connect_h2)
    populate_branches(branches_stress, connect_h2, table)
    count_stress = count_rows(table, connect_h2)
    assert (500000, count_stress)
    clear_table(table, connect_h2)
    count_stress = count_rows(table, connect_h2)
    assert (0, count_stress)


if __name__ == '__main__':
    pytest.main()
