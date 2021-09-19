import pytest
import jaydebeapi
import loan_producer


@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    con = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""], "E:/Program Files (x86)/H2/bin/h2-1.4.200.jar" )
    con.cursor().execute("set schema bytecrunchers")
    con.jconn.setAutoCommit(False)
    return con

def test_get_users(connect_h2):
    #this test will fail if there are no users :<
    conn = connect_h2
    users = loan_producer.get_users(conn)
    assert users
    assert len(users) > 10
    assert users[5][0] #tests the fifth returned user to make sure their id is not 0
    connect_h2.rollback()

def test_create_loan():
    loan = loan_producer.Loan(0, "Test Type")
    assert loan
    assert loan.payment_due #make sure we scheduled a payment

def test_generate_clear(connect_h2):
    conn = connect_h2
    loan_producer.clear(conn)
    cur = conn.cursor()
    query = "SELECT * FROM loans"
    cur.execute(query)
    assert len(cur.fetchall()) == 0 #test clear
    loan_producer.generate_loans(100, conn)
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 100
    assert results[9][2] < 0 #assert that the results (or at least #10) have negative balance
    connect_h2.rollback()