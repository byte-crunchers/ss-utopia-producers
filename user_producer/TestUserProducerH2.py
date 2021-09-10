import pytest

from UserProducer import *

table = "BYTECRUCHERS.USERS"


def test_connect_h2():
    conn_test = connect_h2()
    assert conn_test
    assert isinstance(conn_test, jaydebeapi.Connection)


# This method tests
def test_count_clear_h2():
    conn_count = connect_h2()
    clear_table_h2(table)
    count_test = count_rows_h2(table)
    assert (0, count_test)
    users_count = get_user_data(10)
    populate_users(users_count, conn_count, table)
    count_test = count_rows_h2(table)
    assert (10, count_test)
    clear_table(table)
    count_test = count_rows_h2(table)
    assert (0, count_test)
    conn_count.close()


def test_small_h2():
    conn_small = connect_h2()
    users_small = get_user_data(10)
    clear_table_h2(table)
    populate_users(users_small, conn_small, table)
    count_small = count_rows_h2(table)
    assert (10, count_small)
    clear_table(table)
    count_small = count_rows_h2(table)
    assert (0, count_small)
    conn_small.close()


if __name__ == '__main__':
    pytest.main()
