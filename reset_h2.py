import jaydebeapi


def reset_db():
    con = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:tcp://localhost/~/test;MODE=MySQL", ["sa", ""], "E:/Program Files (x86)/H2/bin/h2-1.4.200.jar" )
    f = open("db-dump.sql")
    con.cursor().execute(f.read())
    con.commit()
    con.close()

if __name__ == "__main__":
    reset_db()
