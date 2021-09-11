import json
import traceback

import jaydebeapi
import mysql
from mysql.connector import Error
from mysql.connector import MySQLConnection


def clear_table(table, clear_conn):
    queries = []
    if isinstance(clear_conn, MySQLConnection):
        queries.append("SET SQL_SAFE_UPDATES = 0;")
        queries.append("delete from {} where 1 = 1;".format(table))
        queries.append("SET SQL_SAFE_UPDATES = 1;")
        queries.append("ALTER TABLE {} AUTO_INCREMENT = 0;".format(table))
    else:
        h2_query = "DELETE FROM {};".format(table)
        queries.append(h2_query)
    try:
        clear_curs = clear_conn.cursor()
        for q in queries:
            clear_curs.execute(q)
    except Error:
        traceback.print_exc()
        print("There was a problem clearing the user table!")
    clear_conn.commit()


# This returns the count of all rows in the table
def count_rows(table, count_conn):
    count_curs = count_conn.cursor()
    count_query = "select count(*) from {}".format(table)
    row_count = None
    try:
        count_curs.execute(count_query)
        row_count = count_curs.fetchall()[0][0]
    except Error:
        traceback.print_exc(
            print("There was a problem counting the rows")
        )
    return row_count
