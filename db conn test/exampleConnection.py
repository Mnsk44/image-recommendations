import DBConnection as db

with db.connect_to_database() as cursor:
    cursor.execute('SELECT version()')
