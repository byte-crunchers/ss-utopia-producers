import jaydebeapi
import pytest
from jaydebeapi import Error
import os
from database_helper import clear_table, count_rows, execute_scripts_from_file
from generate_user_data import get_user_data
from user_producer import populate_users

table = "users"
script_dir = os.path.dirname(__file__)


@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con_try = None
    try:
       con_try = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""], os.environ.get('H2') )
       con_try.jconn.setAutoCommit(False)
       con_try.cursor().execute("set schema bytecrunchers")
    except Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if not isinstance(con_try, jaydebeapi.Connection):
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    else:
        return con_try


def test_drop_schema(connect_h2):
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2DropUsers.sql"), connect_h2)
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2DropBranches.sql"), connect_h2)
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2DropSchema.sql"), connect_h2)
    assert connect_h2
    assert isinstance(connect_h2, jaydebeapi.Connection)
    connect_h2.rollback()


def test_create_schema(connect_h2):
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2CreateSchema.sql"),
                              connect_h2)
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2CreateUsers.sql"),
                              connect_h2)
    execute_scripts_from_file(os.path.join(script_dir, "SQL/H2CreateBranches.sql"),
                              connect_h2)
    connect_h2.rollback()

# This method tests
def test_count_clear(connect_h2):
    clear_table(table, connect_h2)
    count_test = count_rows(table, connect_h2)
    assert (0 == count_test)
    users_count = get_user_data(10)
    populate_users(users_count, connect_h2)
    count_test = count_rows(table, connect_h2)
    assert (10 == count_test)
    clear_table(table, connect_h2)
    count_test = count_rows(table, connect_h2)
    assert (0 == count_test)
    connect_h2.rollback()

def test_large_h2(connect_h2):
    users_large = get_user_data(50)
    clear_table(table, connect_h2)
    populate_users(users_large, connect_h2)
    count_large = count_rows(table, connect_h2)
    assert (50 == count_large)
    clear_table(table, connect_h2)
    count_large = count_rows(table, connect_h2)
    assert (0 == count_large)
    connect_h2.rollback()

if __name__ == '__main__':
    pytest.main()
