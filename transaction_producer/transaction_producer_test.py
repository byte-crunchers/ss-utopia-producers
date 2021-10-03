import pytest
import transaction_producer.transaction_producer as tp
import jaydebeapi


@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""], "E:/Program Files (x86)/H2/bin/h2-1.4.200.jar" )
    con.cursor().execute("set schema bytecrunchers")
    con.jconn.setAutoCommit(False)
    return con


def test_get_accounts(connect_h2):
    #this test will fail if there are no accounts :<
    accounts = tp.get_accounts(connect_h2)
    assert accounts
    assert len(accounts) > 40
    assert accounts[5][0] #tests the fifth returned account to make sure its id is not 0
    connect_h2.rollback()

def test_get_cards(connect_h2):
    cards = tp.get_cards(connect_h2)
    assert cards
    assert len(cards) > 20
    assert cards[5][0] #tests the fifth returned card to make sure its number is not 0


    

def test_generate_clear(connect_h2):
    tp.clear_trans(connect_h2)
    cur = connect_h2.cursor()
    query = 'SELECT * FROM transactions'
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    tp.generate_transactions(200, connect_h2)
    query = 'SELECT * FROM transactions'
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 200
    assert results[9][3] #assert that the results (or at least #10) have a memo
    connect_h2.rollback()

def test_generate_clear_cards(connect_h2):
    tp.clear_card_trans(connect_h2)
    cur = connect_h2.cursor()
    query = 'SELECT * FROM card_transactions'
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    tp.generate_card_transactions(300, connect_h2)
    query = 'SELECT * FROM card_transactions'
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 300
    assert results[9][3] #assert that the results (or at least #10) have a memo
    connect_h2.rollback()