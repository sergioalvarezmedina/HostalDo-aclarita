import cx_Oracle

dsn = "myusername/mypassword@localhost:1521/mydb"

conn = cx_Oracle.connect(dsn)
cur = conn.cursor()
