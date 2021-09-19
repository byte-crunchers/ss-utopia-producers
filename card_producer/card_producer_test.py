import pytest
from card_producer import *

@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""], "E:/Program Files (x86)/H2/bin/h2-1.4.200.jar" )
    con.jconn.setAutoCommit(False)
    con.cursor().execute("set schema bytecrunchers")
    return con


def test_get_accounts(connect_h2):
    #this test will fail if there are no users :<
    conn = connect_h2
    accounts = get_accounts(conn)
    assert accounts
    assert len(accounts) > 50
    assert accounts[5][0] #tests the fifth returned user to make sure their id is not 0
    connect_h2.rollback()


    
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
    
    query = " INSERT INTO users VALUES (1, 'TEST', 'TEST', 'TEST', 'TEST', 'TEST', 0, 0);\
    INSERT INTO accounts VALUES (1, 1, 'Savings', 944.97, 0, null, null, 0, 1)"
    try:
        cur.execute(query)
    except:
        pass #basically  insert  if not exists, so we don't care about the except
    card = Card(1) 
    card.num = 	431923393855046 #gurenteed to be created with this seed
    query = "INSERT INTO cards VALUES (?,?,?,?,?,?)"
    values = (card.account, card.num, card.pin, card.cvc1, card.cvc2, str(card.exp_date))
    cur.execute(query, values)
    generate(50, conn)
    conn.commit()
    query = "SELECT * FROM cards"
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 51
    assert results[9][3] #assert that the results (or at least #10) have a cvc number
    connect_h2.rollback()