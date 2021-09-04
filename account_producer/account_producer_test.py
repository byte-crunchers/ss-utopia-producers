import pytest
from account_producer import *
from mysql.connector import MySQLConnection

def test_connect():
    conn = connect()
    assert conn #not none
    assert isinstance(conn, MySQLConnection)
    conn.close()
    assert not conn.is_connected()

def test_get_users():
    #this test will fail if there are no users :<
    conn = connect()
    users = get_users(conn)
    assert users
    assert len(users) > 10
    assert users[5][0] #tests the fifth returned user to make sure their id is not 0

def test_get_account_types():
    #this test will fail if there are no account types :<
    conn = connect()
    types = get_account_types(conn)
    assert types
    assert len(types) > 5
    assert types[5][0] #tests the fifth returned type to make sure its id is not nuull
    
def test_create_account():
    conn = connect()
    #credit and non-credit accounts have different creation logic, so I must test both
    account_credit = create_account(0, "Test Credit Type")
    account_checking = create_account(0, "Checking")

    assert account_credit
    assert account_credit.payment_due #make sure we scheduled a payment
    assert account_checking
    assert not account_checking.payment_due #as this is a checking account, there should be no payment

def test_generate_clear():
    conn = connect()
    clear(conn)
    cur = conn.cursor()
    query = "SELECT * FROM accounts"
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    generate(10, conn)
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 10
    assert results[9][2] #assert that the results (or at least #10) have account type
