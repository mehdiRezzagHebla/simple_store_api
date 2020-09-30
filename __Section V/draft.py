import sqlite3

db = sqlite3.connect('store.db')
c = db.cursor()
query_delete_name_limit = 'DELETE FROM items WHERE name = ? LIMIT {lim} OFFSET 0'
c.execute(query_delete_name_limit.format(lim=2), ('hat',))
db.commit()
db.close()