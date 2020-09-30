import os
from os.path import dirname, abspath
import sqlite3

path = os.path.join(dirname(dirname(abspath(__file__))), 'first_db.db')


db = sqlite3.connect(path)
cursor = db.cursor()

query = 'SELECT * FROM users'

result = cursor.execute(query)
for row in result:
    print(row)