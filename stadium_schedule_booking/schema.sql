-- has admin and customer details
DROP TABLE IF EXISTS users;

create table users(
    username TEXT NOT NULL UNIQUE,
    emailid TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    favSports TEXT,
    admin TEXT NOT NULL
);

