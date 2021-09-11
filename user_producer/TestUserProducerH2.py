import json

import pytest

import jaydebeapi
from DatabaseHelper import clear_table, count_rows
from GenerateUserData import get_user_data
from UserProducer import populate_users
from jaydebeapi import Error

table = "BYTECRUNCHERS.USERS"


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


def test_connect_h2():
    conn_test = connect_h2()
    assert conn_test
    assert isinstance(conn_test, jaydebeapi.Connection)
    conn_test.close()


# This method tests
def test_count_clear():
    conn_count = connect_h2()
    clear_table(table, conn_count)
    count_test = count_rows(table, conn_count)
    assert (0, count_test)
    users_count = get_user_data(10)
    populate_users(users_count, conn_count, table)
    count_test = count_rows(table, conn_count)
    assert (10, count_test)
    clear_table(table, conn_count)
    count_test = count_rows(table, conn_count)
    assert (0, count_test)
    conn_count.close()


def test_small_h2():
    conn_small = connect_h2()
    users_small = get_user_data(10)
    clear_table(table, conn_small)
    populate_users(users_small, conn_small, table)
    count_small = count_rows(table, conn_small)
    assert (10, count_small)
    clear_table(table, conn_small)
    count_small = count_rows(table, conn_small)
    assert (0, count_small)
    conn_small.close()


def test_large_h2():
    conn_large = connect_h2()
    users_large = get_user_data(5000)
    clear_table(table, conn_large)
    populate_users(users_large, conn_large, table)
    count_large = count_rows(table, conn_large)
    assert (5000, count_large)
    clear_table(table, conn_large)
    count_large = count_rows(table, conn_large)
    assert (0, count_large)
    conn_large.close()


def test_stress_h2():
    conn_stress = connect_h2()
    users_stress = get_user_data(10000)
    clear_table(table, conn_stress)
    populate_users(users_stress, conn_stress, table)
    count_stress = count_rows(table, conn_stress)
    assert (10000, count_stress)
    clear_table(table, conn_stress)
    count_stress = count_rows(table, conn_stress)
    assert (0, count_stress)
    conn_stress.close()


if __name__ == '__main__':
    pytest.main()
