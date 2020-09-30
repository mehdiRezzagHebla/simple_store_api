import sqlite3

db = sqlite3.connect('first_db.db')
c = db.cursor()
#query_delete_name_limit = 'DELETE FROM items WHERE name = ? LIMIT {lim} OFFSET 0'
query_get_items = 'ALTER TABLE items ADD COLUMN store_id INTEGER'
#result = c.execute(query_get_items)
db.commit()
query = 'INSERT INTO items (name, price, store_id) VALUES ("loumja", 10, 1)'
res = c.execute(query)
db.commit()
query = 'SELECT * FROM items'
res = c.execute(query).fetchall()
for row in res:
    print(row)



db.close()