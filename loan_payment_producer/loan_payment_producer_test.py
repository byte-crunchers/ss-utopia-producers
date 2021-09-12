import pytest
import jaydebeapi
import loan_payment_producer as lpp

@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""], "E:/Program Files (x86)/H2/bin/h2-1.4.200.jar" )
    con.cursor().execute("set schema bytecrunchers")
    return con


def test_get_accounts(connect_h2):
    #this test will fail if there are no accounts :<
    accounts = lpp.get_table_id(connect_h2, "accounts")
    assert accounts
    assert len(accounts) > 40
    assert accounts[5][0] #tests the fifth returned account to make sure its id is not 0


def test_get_loans(connect_h2):
    loans = lpp.get_table_id(connect_h2, "loans")
    assert loans
    assert len(loans) > 20
    assert loans[5][0] #tests the fifth returned loan to make sure its id is not 0

def test_generate_clear(connect_h2):
    lpp.clear(connect_h2)
    cur = connect_h2.cursor()
    query = 'SELECT * FROM loan_payments'
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    lpp.generate(200, connect_h2)
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 200
    assert results[9][4] #assert that the results (or at least #10) have a timestamp
