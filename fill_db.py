import os
import sys

import jaydebeapi

import account_producer.account_producer as ap
import branch_producer.branch_producer as bp
import card_producer.card_producer as cp
import loan_payment_producer.loan_payment_producer as lpp
import loan_producer.loan_producer as lp
import transaction_producer.transaction_producer as tp
import user_producer.user_producer as up
import time


def connect_h2():
    con = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""],
                             os.environ.get("H2"))
    con.jconn.setAutoCommit(False)
    return con

class Timer:
    def start(self):
        self.begin = time.perf_counter()
    def stop(self):
        return time.perf_counter() - self.begin
    def print(self, taskname):
        print("task '{:s}' took {:.2f} seconds".format(taskname, self.stop()))

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("please specify either mysql or h2")
    elif sys.argv[1].lower() != "mysql" and sys.argv[1].lower() != "h2":
        print("please specify either mysql or h2")
    else:
        if sys.argv[1].lower() == "mysql":
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
        timer = Timer()
        timer.start()
        up.populate_users(up.get_user_data(300), conn)
        timer.print("pupulate users")
        cur.execute("INSERT INTO account_types VALUES \
            ('Basic Credit', 0.15000, 0.00, 0.0000, 0.0300, 29.00),\
            ('Checking', 0.00000, 0.00, 0.0000, 0.0000, 0.00),\
            ('Fixed Loan', 0.00000, 0.00, 0.0000, 0.0000, 120.00),\
            ('Foodies Credit', 0.00000, 0.00, 0.0040, 0.0100, 29.00),\
            ('Platinum Credit', 0.00000, 200.00, 0.0000, 0.0800, 29.00),\
            ('Plus Credit',0.00000, 0.00, 0.0000, 0.0100, 29.00),\
            ('Savings', 0.00500, 0.00, 0.0000, 0.0000, 0.00);")

        cur.execute("INSERT INTO loan_types VALUES \
            ('Mortgage', 0.078, 0.0312, 45, 96, 360, 1),\
            ('Auto', 0.1392, 0.0324, 25, 24, 96, 1),\
            ('Student', 0.12, 0.03, 35, 60, 300, 0),\
            ('Personal', 0.36, 0.06, 55, 12, 60, 0),\
            ('Payday', 5.16, 3.90, 55, 1, 12, 0);")
        timer.start()
        ap.generate(550, conn)
        timer.print("generate accounts")
        timer.start()
        cp.generate(400, conn)
        timer.print("generate_cards")
        timer.start()
        tp.generate_transactions(200, conn)
        timer.print("generate_transactions")
        timer.start()
        tp.generate_card_transactions(400, conn)
        timer.print("generate_cards")
        timer.start()
        lp.generate_loans(200, conn)
        timer.print("generate loans")
        timer.start()
        lpp.generate(400, conn)
        timer.print("gen loan payments")
        timer.start()
        branches = bp.generate_branches(20)
        bp.clear_table(conn)
        bp.populate_branches(branches, conn)
        timer.print("generate_branches")
        conn.commit()
        conn.close()
