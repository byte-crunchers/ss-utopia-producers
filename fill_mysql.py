import traceback
import jaydebeapi
import json

import user_producer.generate_user_data as generate_ud
import account_producer.account_producer as ap
import card_producer.card_producer as cp
import transaction_producer.transaction_producer as tp
import loan_producer.loan_producer as lp
import loan_payment_producer.loan_payment_producer as lpp
import branch_producer

def populate_users(user_data, pop_conn):
    duplicate_count = 0
    dd_count = 0
    curs = pop_conn.cursor()
    for user in user_data:
        query = "INSERT INTO users(username, email, password, first_name, last_name, is_admin, active) VALUES(?, ?, ?, ?, ?, ?, ?)"
        vals = (generate_ud.generate_username()[0], generate_ud.get_email(user.f_name, user.l_name), user.password, user.f_name, user.l_name, user.is_admin, user.active)
        try:
            curs.execute(query, vals)
        except (jaydebeapi.DatabaseError):  # Check for Duplicates
            traceback.print_exc()
            duplicate_count += 1
            # Find a unique username and email that is not in the database
            while True:
                try:
                    query = "INSERT INTO users(username, email, password, first_name, last_name, is_admin, active) VALUES(?, ?, ?, ?, ?, ?, ?) "
                    vals = (generate_ud.generate_username()[0], generate_ud.get_email(user.f_name, user.l_name), user.password, user.f_name, user.l_name, user.is_admin, user.active)
                    curs.execute(query, vals)
                    break
                except (jaydebeapi.DatabaseError):
                    dd_count += 1
                    continue

if __name__ == "__main__":
    conn = ap.connect("dbkey.json")
    cur = conn.cursor()
    schema = open("schema_mysql.sql")
    for line in schema.read().split(";"):
        if line == '' or line.isspace():
            break
        cur.execute(line)
    
    users_list = generate_ud.get_user_data(10)
    populate_users(users_list, conn)

    cur.execute("INSERT INTO account_types VALUES \
    ('Basic Credit', 0.15000, 0.00, 0.0000, 0.0300, 29.00),\
('Checking', 0.00000, 0.00, 0.0000, 0.0000, 0.00),\
('Fixed Loan', 0.00000, 0.00, 0.0000, 0.0000, 120.00),\
('Foodies Credit', 0.00000, 0.00, 0.0040, 0.0100, 29.00),\
('Platinum Credit', 0.00000, 200.00, 0.0000, 0.0800, 29.00),\
('Plus Credit',0.00000, 0.00, 0.0000, 0.0100, 29.00),\
('Savings', 0.00500, 0.00, 0.0000, 0.0000, 0.00);")


    ap.generate(1, conn)


