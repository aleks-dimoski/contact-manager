# Manager to handle sql queries and provide framework for adding/removing data

import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "pi",
    password = "PASSWORD",
    database = "contactList"
)

curs = mydb.cursor(buffered=True)

def gen_tables():
    curs.execute("SET FOREIGN_KEY_CHECKS=0")
    curs.execute("DROP TABLE person")
    curs.execute("DROP TABLE org")
    curs.execute("DROP TABLE contacts")
    curs.execute("DROP TABLE PORelations")
    curs.execute("DROP TABLE PCRelations")
    curs.execute("SET FOREIGN_KEY_CHECKS=1")
    curs.execute("CREATE TABLE person (PersId INT AUTO_INCREMENT PRIMARY KEY NOT NULL, fname VARCHAR(255) NOT NULL, lname VARCHAR(255) NOT NULL, attention INT, bday DATE, married DATE, spouseId INT)")
    curs.execute("ALTER TABLE person ADD FOREIGN KEY (spouseID) REFERENCES person(PersId)")
    curs.execute("CREATE TABLE org (OrgId INT AUTO_INCREMENT PRIMARY KEY NOT NULL, name VARCHAR(255) NOT NULL, type VARCHAR(127), description VARCHAR(1023))")
    curs.execute("CREATE TABLE contacts (ContId INT AUTO_INCREMENT PRIMARY KEY NOT NULL, email VARCHAR(255), phone VARCHAR(32), street VARCHAR(255), city VARCHAR(255), zcode VARCHAR(255))")
    curs.execute("CREATE TABLE PORelations (POId INT AUTO_INCREMENT PRIMARY KEY NOT NULL, PersID INT, OrgID INT, FOREIGN KEY (PersID) REFERENCES person(PersID), FOREIGN KEY (OrgID) REFERENCES org(OrgId))")
    curs.execute("CREATE TABLE PCRelations (PCId INT AUTO_INCREMENT PRIMARY KEY NOT NULL, PersId INT, ContId INT, FOREIGN KEY (PersId) REFERENCES person(PersId), FOREIGN KEY (ContId) REFERENCES contacts(ContId) ON DELETE CASCADE)")

def print_cursor(cursor):
    for i in cursor:
         print(i)

def print_people():
    curs.execute("SELECT * FROM person")
    print_cursor(curs)

def add_person(**kwargs):
    try:
        ins = "INSERT INTO person ("
        form = '('
        vals = []
        for key, val in kwargs.items():
            ins += key + ', '
            vals += [val]
            form += '%s, '
        ins = ins[:-2] + ') VALUES (' + ('%s, '*len(vals))[:-2]+')'
        vals = tuple(vals)
        curs.execute(ins, vals)
        mydb.commit()
    except:
        raise Exception("Invalid INSERT INTO Query. Valid arguments are listed below. You may be missing required data.\n" + str(get_cols("person")))

def print_tables():
    curs.execute("SHOW TABLES")
    for table in curs:
        print('\nSHOW columns FROM '+str(table)[2:-3])
        mycols = get_cols(str(table)[2:-3])
        print(mycols)

def get_cols(table):
    mycols = mydb.cursor(buffered=True)
    cols = []
    hold = []
    mycols.execute("SHOW columns FROM " + table)
    for col in mycols:
        hold += col
    for ind, val in enumerate(hold):
        if ind%6 == 0:
            cols += [val]
    return cols

#print_tables()

#add_person(fname='Bob', lname='Beegus', brogus='bb')
print_people()
