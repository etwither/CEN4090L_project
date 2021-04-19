import sqlite3

conn = sqlite3.connect('storeData.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE Reviews (Username VARCHAR(40), Game VARCHAR(50), ReviewTime DATETIME, Rating FLOAT, Review VARCHAR(500))')

print ("Table created successfully")
conn.close()
