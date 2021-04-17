import sqlite3

conn = sqlite3.connect('storeData.db')

conn.execute('CREATE TABLE Reviews (Username VARCHAR(40), Game VARCHAR(50), ReviewTime DATETIME, Rating FLOAT, Review VARCHAR(500))')

conn.close()

