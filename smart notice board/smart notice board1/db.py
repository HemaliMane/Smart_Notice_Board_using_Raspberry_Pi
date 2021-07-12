import sqlite3
global d


db = sqlite3.connect('test.db;')
cursor = db.cursor()
cursor.execute("create table if not exists noticee(id INTEGER PRIMARY KEY, data TEXT)") 
  

self.d = StringVar()
db = sqlite3.connect('test.db;')
cursor = db.cursor()
cursor.execute("select * from noticee ORDER BY id DESC LIMIT 2")
user = cursor.fetch()
self.d = user[2]
print(self.d)
