import json

import pytest

import jaydebeapi
from database_helper import clear_table, count_rows, execute_scripts_from_file
from generate_user_data import get_user_data
from user_producer import populate_users
from jaydebeapi import Error

table = "BYTECRUNCHERS.USERS"


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
    execute_scripts_from_file("C:/Users/meeha/OneDrive/Desktop/SmoothStack/ByteCrunchersSQL/H2DropUsers.sql", connect_h2)
    execute_scripts_from_file("C:/Users/meeha/OneDrive/Desktop/SmoothStack/ByteCrunchersSQL/H2DropBranches.sql", connect_h2)
    execute_scripts_from_file("C:/Users/meeha/OneDrive/Desktop/SmoothStack/ByteCrunchersSQL/H2DropSchema.sql", connect_h2)
    assert connect_h2
    assert isinstance(connect_h2, jaydebeapi.Connection)


def test_create_schema(connect_h2):
    execute_scripts_from_file("C:/Users/meeha/OneDrive/Desktop/SmoothStack/ByteCrunchersSQL/H2CreateSchema.sql",
                              connect_h2)
    execute_scripts_from_file("C:/Users/meeha/OneDrive/Desktop/SmoothStack/ByteCrunchersSQL/H2CreateUsers.sql",
                              connect_h2)
    execute_scripts_from_file("C:/Users/meeha/OneDrive/Desktop/SmoothStack/ByteCrunchersSQL/H2CreateBranches.sql",
                              connect_h2)
    assert connect_h2
    assert isinstance(connect_h2, jaydebeapi.Connection)


# This method tests
def test_count_clear(connect_h2):
    clear_table(table, connect_h2)
    count_test = count_rows(table, connect_h2)
    assert (0, count_test)
    users_count = get_user_data(10)
    populate_users(users_count, connect_h2, table)
    count_test = count_rows(table, connect_h2)
    assert (10, count_test)
    clear_table(table, connect_h2)
    count_test = count_rows(table, connect_h2)
    assert (0, count_test)


def test_small_h2(connect_h2):
    users_small = get_user_data(10)
    clear_table(table, connect_h2)
    populate_users(users_small, connect_h2, table)
    count_small = count_rows(table, connect_h2)
    assert (10, count_small)
    clear_table(table, connect_h2)
    count_small = count_rows(table, connect_h2)
    assert (0, count_small)


def test_large_h2(connect_h2):
    users_large = get_user_data(500)
    clear_table(table, connect_h2)
    populate_users(users_large, connect_h2, table)
    count_large = count_rows(table, connect_h2)
    assert (500, count_large)
    clear_table(table, connect_h2)
    count_large = count_rows(table, connect_h2)
    assert (0, count_large)


def test_stress_h2(connect_h2):
    users_stress = get_user_data(10000)
    clear_table(table, connect_h2)
    populate_users(users_stress, connect_h2, table)
    count_stress = count_rows(table, connect_h2)
    assert (10000, count_stress)
    clear_table(table, connect_h2)
    count_stress = count_rows(table, connect_h2)
    assert (0, count_stress)


if __name__ == '__main__':
    pytest.main()
