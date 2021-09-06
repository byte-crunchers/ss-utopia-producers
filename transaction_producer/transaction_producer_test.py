import pytest
from transaction_producer import *
from mysql.connector import MySQLConnection

def test_connect():
    conn = connect()
    assert conn #not none
    assert isinstance(conn, MySQLConnection)
    conn.close()
    assert not conn.is_connected()

def test_get_accounts():
    #this test will fail if there are no accounts :<
    conn = connect()
    accounts = get_accounts(conn)
    assert accounts
    assert len(accounts) > 500
    assert accounts[5][0] #tests the fifth returned account to make sure its id is not 0
    conn.close()

    
def test_get_cards():
    conn = connect()
    cards = get_cards(conn)
    assert cards
    assert len(cards) > 500
    assert cards[5][1] #tests the fifth returned card to make sure its number is not 0
    conn.close()

    


def test_generate_clear():
    conn = connect()
    clear_trans(conn)
    cur = conn.cursor()
    query = "SELECT * FROM transactions"
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    generate_transactions(500, conn)
    query = "SELECT * FROM transactions"
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 500
    assert results[9][3] #assert that the results (or at least #10) have a memo


def test_generate_clear_cards():
    
    conn = connect()
    clear_card_trans(conn)
    cur = conn.cursor()
    query = "SELECT * FROM card_transactions"
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    generate_card_transactions(500, conn)
    query = "SELECT * FROM card_transactions"
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 500
    assert results[9][3] #assert that the results (or at least #10) have a memo



if __name__ == "__main__":
    test_generate_clear()
    test_generate_clear_cards()