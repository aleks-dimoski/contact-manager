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
    curs.execute("CREATE TABLE person (ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, fname VARCHAR(255) NOT NULL, lname VARCHAR(255) NOT NULL, attention INT, bday DATE, married DATE, spouseId INT)")
    curs.execute("ALTER TABLE person ADD FOREIGN KEY (spouseID) REFERENCES person(ID)")
    curs.execute("CREATE TABLE org (ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, name VARCHAR(255) NOT NULL, type VARCHAR(127), description VARCHAR(1023))")
    curs.execute("CREATE TABLE contacts (ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, email VARCHAR(255), phone VARCHAR(32), street VARCHAR(255), city VARCHAR(255), zcode VARCHAR(255), main BIT)")
    curs.execute("CREATE TABLE PORelations (ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, PersID INT, OrgID INT, FOREIGN KEY (PersID) REFERENCES person(ID), FOREIGN KEY (OrgID) REFERENCES org(ID))")
    curs.execute("CREATE TABLE PCRelations (ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, PersId INT, ContId INT, FOREIGN KEY (PersId) REFERENCES person(ID), FOREIGN KEY (ContId) REFERENCES contacts(ID) ON DELETE CASCADE)")

def print_cursor(cursor):
    for i in cursor:
         print(i)

def print_table_data(table=""):
    curs.execute("SELECT * FROM "+table)
    print("Table",table)
    print_cursor(curs)

def insert_entry(**kwargs):
    try:
        ins = "INSERT INTO " + kwargs['table'] + " ("
        form = '('
        vals = []
        for key, val in kwargs.items():
            if not key == 'table':
                ins += key + ', '
                vals += [val]
                form += '%s, '
        ins = ins[:-2] + ') VALUES (' + ('%s, '*len(vals))[:-2]+')'
        vals = tuple(vals)

        curs.execute(ins, vals)
        mydb.commit()
    except:
        raise Exception("Invalid INSERT INTO Query. Valid arguments are listed below. You may be missing required data.\n" + str(get_cols(kwargs['table']))+"\nSee the query below\n" + ins%vals)

def print_tables():
    curs.execute("SHOW TABLES")
    for table in curs:
        print('\nSHOW columns FROM '+str(table)[2:-3])
        mycols = get_cols(str(table)[2:-3])
        print(mycols)

def get_tables():
    curs.execute("SHOW TABLES")
    tables = [str(table)[2:-3] for table in curs]
    tables = {table:get_cols(table) for table in tables}
    return tables

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

def latest_id(table):
    curs.execute("SELECT MAX(ID) FROM " + table)
    for i in curs:
        return int(str(i)[1:-2])

''' Testing '''
#print_tables()

#add_person(fname='Bob', lname='Beegus', brogus='bb')
#print_people()

#print_table_data(table='person')
#print_table_data(table='org')
gen_tables()
