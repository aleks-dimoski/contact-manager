import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "pi",
    password = "PASSWORD",
    database = "contactList"
)

curs = mydb.cursor()

curs.execute("SHOW TABLES")

for i in curs:
    print(i)
