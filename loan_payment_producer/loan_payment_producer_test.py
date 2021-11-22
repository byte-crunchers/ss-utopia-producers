import os

import jaydebeapi
import pytest

import loan_payment_producer as lpp


@pytest.fixture(scope="module", autouse=True)
def connect_h2():
    conn = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL;database_to_upper=false"
                                               "", ["sa", ""],
                              os.environ.get("H2"))
    conn.cursor().execute("set schema bytecrunchers")
    conn.jconn.setAutoCommit(False)
    return conn


def test_get_accounts(connect_h2):
    # this test will fail if there are no accounts :<
    accounts = lpp.get_table_id(connect_h2, "accounts")
    assert accounts
    assert len(accounts) > 40
    assert accounts[5][0]  # tests the fifth returned account to make sure its id is not 0
    connect_h2.rollback()


def test_get_loans(connect_h2):
    loans = lpp.get_table_id(connect_h2, "loans")
    assert loans
    assert len(loans) > 15
    assert loans[5][0]  # tests the fifth returned loan to make sure its id is not 0
    connect_h2.rollback()


def test_generate_clear(connect_h2):
    lpp.clear(connect_h2)
    cur = connect_h2.cursor()
    query = 'SELECT * FROM loan_payments'
    cur.execute(query)
    assert len(cur.fetchall()) == 0  # test clear
    lpp.generate(100, connect_h2)
    cur.execute(query)
    results = cur.fetchall()
    assert len(results) == 100
    assert results[9][4]  # assert that the results (or at least #10) have a timestamp
    connect_h2.rollback()


if __name__ == '__main__':
    pytest.main()
