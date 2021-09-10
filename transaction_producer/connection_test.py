from transaction_producer import connect
def test_connect():
    conn = connect()
    assert conn #not none
    conn.close()