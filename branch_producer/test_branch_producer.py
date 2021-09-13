import json

import jaydebeapi
import pytest
from jaydebeapi import Error

from branch_producer import generate_branches
from branch_producer import populate_branches
from database_helper import clear_table, count_rows, execute_scripts_from_file

table = "BYTECRUNCHERS.BRANCHES"


# This method connects to a h2 database
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


def test_create_schema():
    conn_create = connect_h2()
    execute_scripts_from_file("C:/Users/meeha/OneDrive/Desktop/SmoothStack/ByteCrunchersSQL/H2CreateSchema.sql",
                              connect_h2())
    execute_scripts_from_file("C:/Users/meeha/OneDrive/Desktop/SmoothStack/ByteCrunchersSQL/H2CreateUsers.sql",
                              connect_h2())
    execute_scripts_from_file("C:/Users/meeha/OneDrive/Desktop/SmoothStack/ByteCrunchersSQL/H2CreateBranches.sql",
                              connect_h2())
    conn_create.close()

def test_count_clear():
    conn_count = connect_h2()
    clear_table(table, conn_count)
    count_test = count_rows(table, conn_count)
    assert (0, count_test)
    branches_count = generate_branches(10)
    populate_branches(branches_count, conn_count, table)
    count_test = count_rows(table, conn_count)
    assert (10, count_test)
    clear_table(table, conn_count)
    count_test = count_rows(table, conn_count)
    assert (0, count_test)
    conn_count.close()


def test_small():
    conn_small = connect_h2()
    branches_small = generate_branches(10)
    clear_table(table, conn_small)
    populate_branches(branches_small, conn_small, table)
    count_small = count_rows(table, conn_small)
    assert (10, count_small)
    clear_table(table, conn_small)
    count_small = count_rows(table, conn_small)
    assert (0, count_small)
    conn_small.close()


def test_large():
    conn_large = connect_h2()
    branches_large = generate_branches(1000)
    clear_table(table, conn_large)
    populate_branches(branches_large, conn_large, table)
    count_large = count_rows(table, conn_large)
    assert (1000, count_large)
    clear_table(table, conn_large)
    count_large = count_rows(table, conn_large)
    assert (0, count_large)
    conn_large.close()


def test_stress():
    conn_stress = connect_h2()
    branches_stress = generate_branches(500000)
    clear_table(table, conn_stress)
    populate_branches(branches_stress, conn_stress, table)
    count_stress = count_rows(table, conn_stress)
    assert (500000, count_stress)
    clear_table(table, conn_stress)
    count_stress = count_rows(table, conn_stress)
    assert (0, count_stress)
    conn_stress.close()


if __name__ == '__main__':
    pytest.main()
