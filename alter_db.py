import sqlite3

db = sqlite3.connect('first_db.db')

cursor = db.cursor()
try:
    query = 'CREATE TABLE IF NOT EXISTS stores (id INTEGER PRIMARY KEY, name text)'
    cursor.execute(query)
except:
    pass


add_default_item_query = 'INSERT INTO items(name, price) VALUES (?, ?)'
cursor.execute(add_default_item_query, ('chBelt', '50'))
db.commit()

request_items_query = 'Select * From items WHERE name = "chsBelt"'
result = cursor.execute(request_items_query)


delete_specific_users_query = 'DELETE FROM users WHERE username=?'
#users_delete = [
 #   ('Kenza',),
  #  ('hamouda',)
#]
#cursor.executemany(delete_specific_users_query, users_delete)

request_users_query = 'Select * From users'
result = cursor.execute(request_users_query)
for user in result:
    print(user)


db.commit()
db.close()