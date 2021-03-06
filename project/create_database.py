import sqlite3
from datetime import datetime

conn = sqlite3.connect('database.db')
print('open database successfully')

conn.execute('PRAGMA foreign_keys = 1;')

conn.execute('CREATE TABLE user \
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
            username VARCHAR(256) NOT NULL, \
            email VARCHAR(1024) NOT NULL, \
            password VARVARCHAR(255) NOT NULL, \
            created_at VARCHAR(64) NOT NULL);')

conn.execute('CREATE TABLE article \
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
            user_id INTEGER REFERENCES user(id) ON UPDATE CASCADE, \
            title VARCHAR(1024) NOT NULL, \
            content TEXT NOT NULL, \
            created_at VARCHAR(64) NOT NULL); ')

print('table created successfully')

conn.close()
