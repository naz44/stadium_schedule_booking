import sqlite3
import hashlib
from creds import admin_pass
connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)", 
('admin1','alzaha2427@gmail.com',str(hashlib.md5(admin_pass.encode()).hexdigest()),'admin1','ad1',None,'yes'))

cur.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",('admin2','jjtjasonthomas@gmail.com',str(hashlib.md5(admin_pass.encode()).hexdigest()),'admin2','ad2',None,'yes'))

cur.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",('admin3','ashishmanghani45@gmail.com',str(hashlib.md5(admin_pass.encode()).hexdigest()),'admin3','ad3',None,'yes'))

cur.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",('admin4','vudaykumar.777@gmail.com',str(hashlib.md5(admin_pass.encode()).hexdigest()),'admin4','ad4',None,'yes'))

cur.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",('admin5','sarveshpaul@gmail.com',str(hashlib.md5(admin_pass.encode()).hexdigest()),'admin5','ad5',None,'yes'))

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

cur.execute("INSERT INTO sports (id, name, cost, status, remarks) VALUES (?,?,?,?,?)",
('10','Volleyball','1050','y',''))

connection.commit()
connection.close()