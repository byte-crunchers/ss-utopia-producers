import os

import jaydebeapi
import pytest
from cryptography.fernet import Fernet
import json

from user_producer import populate_users, execute_scripts_from_file, get_user_data, get_secret

script_dir = os.path.dirname(__file__)
schema_path = os.path.join(script_dir, "../schema_h2.sql")


@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con_try = None
    try:
        con_try = jaydebeapi.connect("org.h2.Driver",
                                     "jdbc:h2:tcp://localhost/~/test;MODE=MySQL;database_to_upper=false",
                                     ["sa", ""],
                                     os.environ.get('H2'))
        con_try.jconn.setAutoCommit(False)
        con_try.cursor().execute("set schema bytecrunchers")
    except jaydebeapi.Error:
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    if not isinstance(con_try, jaydebeapi.Connection):
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    else:
        return con_try


# Test connection and create the schema
def test_create_schema(connect_h2):
    execute_scripts_from_file(schema_path, connect_h2)
    assert connect_h2
    connect_h2.rollback()


def test_populate_small(connect_h2):
    curs = connect_h2.cursor()
    curs.execute("DELETE FROM users")  # Clear Table
    curs.execute("SELECT COUNT(*) FROM users")  # Get row count of table
    assert (0 == curs.fetchmany(size=1)[0][0])  # Test that the table is empty
    populate_users(get_user_data(100), connect_h2)  # Add users to table
    curs.execute("SELECT COUNT(*) FROM users")  # Get row count of table
    assert (100 == curs.fetchmany(size=1)[0][0])  # Test that the users where added
    curs.execute("DELETE FROM users")  # Clear Table
    curs.execute("SELECT COUNT(*) FROM users")  # Get row count of table
    assert (0 == curs.fetchmany(size=1)[0][0])  # Test that the table is empty
    connect_h2.rollback()


def test_populate_large(connect_h2):
    curs = connect_h2.cursor()
    curs.execute("DELETE FROM users")  # Clear Table
    curs.execute("SELECT COUNT(*) FROM users")  # Get row count of table
    assert (0 == curs.fetchmany(size=1)[0][0])  # Test that the table is empty
    populate_users(get_user_data(1000), connect_h2)  # Add users to table
    curs.execute("SELECT COUNT(*) FROM users")  # Get row count of table
    assert (1000 == curs.fetchmany(size=1)[0][0])  # Test that the users where added
    curs.execute("DELETE FROM users")  # Clear Table
    curs.execute("SELECT COUNT(*) FROM users")  # Get row count of table
    assert (0 == curs.fetchmany(size=1)[0][0])  # Test that the table is empty
    connect_h2.rollback()


def test_ssn_encrypt(connect_h2):
    curs = connect_h2.cursor()
    test_user_list = get_user_data(1)
    curs.execute("DELETE FROM users")
    populate_users(test_user_list, connect_h2)
    curs.execute("SELECT * FROM users")
    user = curs.fetchall()[0]
    dec_ssn = test_user_list[0].unc_ssn
    enc_ssn = user[7]
    secret_name = user[17]
    username = user[1]
    secret_json_string = get_secret(secret_name)
    json_data = json.loads(secret_json_string)
    key = (json_data[username]) # Printing key
    fernet = Fernet(key)
    decoded_ssn = fernet.decrypt(stringToBase64(enc_ssn)).decode()
    assert (decoded_ssn == dec_ssn)


def stringToBase64(s):
    return s.encode('utf-8')


if __name__ == '__main__':
    pytest.main()


