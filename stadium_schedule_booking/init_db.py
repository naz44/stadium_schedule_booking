import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)", 
('admin1','alzaha2427@gmail.com','admin@123','Nz','sk',None,'yes'))

cur.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",('admin2','jjtjasonthomas@gmail.com','admin@456','J','T',None,'yes'))

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('1','Football','2000','y',''))

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('2','Cricket','1500','y',''))

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('3','Hockey','1800','y',''))

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('4','Rugby','1200','y',''))

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('5','Basketball','2000','y',''))

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('6','Tennis','1600','y',''))

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('7','Badminton','800','y',''))

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('8','Archery','1200','y',''))

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('9','Golf','2100','y',''))

connection.commit()
connection.close()