-- has admin and customer details
DROP TABLE IF EXISTS users;

create table users(
    username TEXT NOT NULL UNIQUE,
    emailid TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    favsports TEXT,
    admin TEXT NOT NULL
);
--has sports details
DROP TABLE IF EXISTS sports;

create table sports(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    cost INTEGER,
    status TEXT,
    remarks TEXT
);
--has booking details
DROP TABLE IF EXISTS booking;

create table booking(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sportsId INTEGER,
    date DATETIME,
    duration INTEGER,
    total cost DECIMAL(7,2),
    customer username TEXT,
    code TEXT,
    FOREIGN KEY(sportsId) REFERENCES sports(id)
);

DROP TABLE IF EXISTS maintenance;

create table maintenance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sportsId INTEGER,
    date DATETIME,
    duration INTEGER,
    customer_username TEXT,
    code TEXT,
    comment TEXT,
    FOREIGN KEY(sportsId) REFERENCES sports(id)
);
