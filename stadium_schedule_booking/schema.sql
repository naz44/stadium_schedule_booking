-- has admin and customer details
 DROP TABLE IF EXISTS users;
 DROP TABLE IF EXISTS sports;

create table users(
    username TEXT NOT NULL UNIQUE,
    emailid TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    favsports TEXT,
    admin TEXT NOT NULL
);

create table sports(
    id VARCHAR PRIMARY KEY,
    name TEXT UNIQUE,
    cost INT,
    status TEXT,
    remarks TEXT
);



