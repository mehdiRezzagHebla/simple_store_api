import sqlite3

# first create connection
connection = sqlite3.connect('first_db.db')

# second create cursor
cursor = connection.cursor()

# third create table
create_statement = 'CREATE TABLE users (id integer PRIMARY KEY, username text, password text)'
cursor.execute(create_statement)

# create user & insert it into our users table
user = ('mehdi', 'azer')
insert_user_statement = 'INSERT INTO users(username, password) VALUES (?, ?)'
cursor.execute(insert_user_statement, user)

# create multiple users & insert them into our users table
users = [
    ('Lydia', 'Mistress'),
    ('Kenza', 'Dominatrix')
]
cursor.executemany(insert_user_statement, users)
# commit changes
connection.commit()
# retrieve data from table
retrieve_statement = 'SELECT * FROM users'
rows = cursor.execute(retrieve_statement)

for row in rows:
    print(row)

# close db
connection.close()
