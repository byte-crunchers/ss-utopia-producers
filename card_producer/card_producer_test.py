import pytest
from card_producer import *

@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""], "E:/Program Files (x86)/H2/bin/h2-1.4.200.jar" )
    con.cursor().execute("set schema bytecrunchers")
    return con


def test_get_accounts(connect_h2):
    #this test will fail if there are no users :<
    conn = connect_h2
    accounts = get_accounts(conn)
    assert accounts
    assert len(accounts) > 50
    assert accounts[5][0] #tests the fifth returned user to make sure their id is not 0


    
def test_card():
    card1 = Card(1)
    card1.build_number()
    card2 = Card(2)
    card2.build_number()
    assert card1
    assert card1.num
    assert card1.num != card2.num

def test_generate_clear(connect_h2):
    random.seed(42069)
    conn = connect_h2
    clear(conn)
    cur = conn.cursor()
    query = "SELECT * FROM cards"
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    #force a card_num collision, a 1/1,000,000,000 chance
    card = Card(1) #with this seed, account 1 has no card. Therefor SQL will not reject it
    card.num = 2319231456914939 #gurenteed to be created with this seed
    query = "INSERT INTO cards VALUES (?,?,?,?,?,?)"
    values = (card.account, card.num, card.pin, card.cvc1, card.cvc2, str(card.exp_date))
    cur.execute(query, values)

    generate(50, conn)
    query = "SELECT * FROM cards"
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 51
    assert results[9][3] #assert that the results (or at least #10) have a cvc number
