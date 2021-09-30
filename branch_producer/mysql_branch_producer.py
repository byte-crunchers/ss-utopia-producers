import os
import traceback

import jaydebeapi
from mysql.connector import Error

from branch_producer import generate_branches, populate_branches

# Environment Variables
mysql_pass = os.environ.get("MYSQL_PASS")
mysql_user = os.environ.get("MYSQL_USER")
mysql_jar = os.environ.get("MYSQL_JAR")
mysql_loc = os.environ.get("MYSQL_LOC")
# Relative Paths
script_dir = os.path.dirname(__file__)


def connect():
    con_try = None
    try:
        con_try = jaydebeapi.connect("com.mysql.cj.jdbc.Driver", mysql_loc,
                                     [mysql_user, mysql_pass], mysql_jar)
        con_try.jconn.setAutoCommit(False)
    except Error:
        traceback.print_exc()
        print("There was a problem connecting to the database, please make sure the database information is correct!")
    return con_try


if __name__ == '__main__':
    conn = connect()
    branches_small = generate_branches(100)
    populate_branches(branches_small, conn)
    conn.commit()
    conn.close()
