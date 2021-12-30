import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)", 
('admin1','alzaha2427@gmail.com','admin@123','Nz','sk','random','yes'))

cur.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",('admin2','jjtjasonthomas@gmail.com','admin@456','J','T','random','yes'))


connection.commit()
connection.close()