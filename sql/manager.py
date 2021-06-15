import os
from sql_connection import *

valid_coms = {'insert':insert_entry, 'delete':'Unimplemented', 'update':'Unimplemented', 'select':'Unimplemented'}

def gen_query(**kwargs):
    try:
        tables = kwargs['tables']
        command = kwargs['com']
        for table in tables:
            valid_cols = get_cols(table)
            query_hold = {key:val for (key,val) in kwargs.items() if key in valid_cols}
            query_hold['table'] = table
            valid_coms[command](**query_hold)
        if 'person' in tables and 'contacts' in tables:
            valid_coms[command](table='PCRelations',PersId=latest_id('person'),ContId=latest_id('contacts'))
        if 'person' in tables and 'org' in tables:
            valid_coms[command](table='PORelations',PersId=latest_id('person'),OrgId=latest_id('org'))

    except:
        raise Exception("Invalid Query.")


gen_query(tables=['person','contacts'],com='insert',fname='Jamiesss',lname='Eldritch',phone='123-456-7890')
gen_query(tables=['person','org','contacts'],com='insert',fname='Brian',lname='Worm',phone='111-111-1234',name='The Lodge 804',type='Fraternity', main=True)

print_table_data(table='person')
print_table_data(table='contacts')
print_table_data(table='org')
print_table_data(table='PCRelations')
print_table_data(table='PORelations')
latest_id('person')

