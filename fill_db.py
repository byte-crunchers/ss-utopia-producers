import sys
import traceback
import jaydebeapi
import os

import user_producer.user_producer as up
import account_producer.account_producer as ap
import card_producer.card_producer as cp
import transaction_producer.transaction_producer as tp
import loan_producer.loan_producer as lp
import loan_payment_producer.loan_payment_producer as lpp
import branch_producer.branch_producer as bp

def connect_h2():
    con = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""], os.environ.get("H2") )
    con.jconn.setAutoCommit(False)
    return con



if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("please specify either mysql or h2")
    elif sys.argv[1].lower() != "mysql" and sys.argv[1].lower() != "h2":
        print("please specify either mysql or h2")
    else:
        if(sys.argv[1].lower() == "mysql"):
            conn = ap.connect()
            schema = open("schema_mysql.sql")
        else:
            conn = connect_h2()
            schema = open("schema_h2.sql")

        cur = conn.cursor()
        for line in schema.read().split(";"):
            if line == '' or line.isspace():
                break
            cur.execute(line)
        
        up.populate_users(up.get_user_data(100), conn)

        cur.execute("INSERT INTO account_types VALUES \
            ('Basic Credit', 0.15000, 0.00, 0.0000, 0.0300, 29.00),\
            ('Checking', 0.00000, 0.00, 0.0000, 0.0000, 0.00),\
            ('Fixed Loan', 0.00000, 0.00, 0.0000, 0.0000, 120.00),\
            ('Foodies Credit', 0.00000, 0.00, 0.0040, 0.0100, 29.00),\
            ('Platinum Credit', 0.00000, 200.00, 0.0000, 0.0800, 29.00),\
            ('Plus Credit',0.00000, 0.00, 0.0000, 0.0100, 29.00),\
            ('Savings', 0.00500, 0.00, 0.0000, 0.0000, 0.00);")

        cur.execute("INSERT INTO loan_types VALUES \
            ('Morgage', 0.04, 0.004, 300, 120, 360),\
            ('Auto', 0.05, 0.00499, 70, 12, 72),\
            ('Student', 0.03, 0.0035, 200, 60, 180);")

        ap.generate(100, conn)

        cp.generate(70, conn)

        tp.generate_transactions(200, conn)
        tp.generate_card_transactions(400, conn)

        lp.generate_loans(200, conn)

        lpp.generate(80, conn)

        branches = bp.generate_branches(20)
        bp.clear_table(conn)
        bp.populate_branches(branches, conn)

        conn.commit()
        conn.close()
        


