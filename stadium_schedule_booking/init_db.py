import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO admin (username,emailid,password) VALUES (?, ?,?)",('admin1','alzaha2427@gmail.com','admin@123'))

cur.execute("INSERT INTO admin (username,emailid,password) VALUES (?, ?,?)",('admin2','jjtjasonthomas@gmail.com','admin@456'))



connection.commit()
connection.close()