import pytest
import os
from account_producer import *


@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""], os.environ.get("H2") )
    con.cursor().execute("set schema bytecrunchers")
    con.jconn.setAutoCommit(False)
    return con

def test_get_users(connect_h2):
    #this test will fail if there are no users :<
    conn = connect_h2
    users = get_users(conn)
    assert users
    assert len(users) > 10
    assert users[5][0] #tests the fifth returned user to make sure their id is not 0
    conn.rollback()

def test_get_account_types(connect_h2):
    #this test will fail if there are no account types :<
    conn = connect_h2
    types = get_account_types(conn)
    assert types
    assert len(types) > 5
    assert types[5][0] #tests the fifth returned type to make sure its id is not nuull
    conn.rollback()

def test_create_account():
    #credit and non-credit accounts have different creation logic, so I must test both
    account_credit = create_account(0, "Test Credit Type")
    account_checking = create_account(0, "Checking")

    assert account_credit
    assert account_credit.payment_due #make sure we scheduled a payment
    assert account_checking
    assert not account_checking.payment_due #as this is a checking account, there should be no payment

def test_generate_clear(connect_h2):
    conn = connect_h2
    clear(conn)
    cur = conn.cursor()
    query = "SELECT * FROM accounts"
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    generate(100, conn)
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 100
    assert results[9][2] #assert that the results (or at least #10) have account type
    conn.rollback()