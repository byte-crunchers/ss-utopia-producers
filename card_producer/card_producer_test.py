import pytest
from card_producer import *
from mysql.connector import MySQLConnection

def test_connect():
    conn = connect()
    assert conn #not none
    assert isinstance(conn, MySQLConnection)
    conn.close()
    assert not conn.is_connected()

def test_get_accounts():
    #this test will fail if there are no users :<
    conn = connect()
    accounts = get_accounts(conn)
    assert accounts
    assert len(accounts) > 500
    assert accounts[5][0] #tests the fifth returned user to make sure their id is not 0
    conn.close()

    
def test_card():
    card1 = Card(1)
    card1.build_number()
    card2 = Card(2)
    card2.build_number()
    assert card1
    assert card1.num
    assert card1.num != card2.num

def test_generate_clear():
    conn = connect()
    clear(conn)
    cur = conn.cursor()
    query = "SELECT * FROM cards"
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    generate(500, conn)
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 500
    assert results[9][3] #assert that the results (or at least #10) have a cvc number
