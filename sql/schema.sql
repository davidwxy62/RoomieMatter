PRAGMA foreign_keys = ON;

CREATE TABLE users
(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(40) NOT NULL UNIQUE,
    "password" VARCHAR (256) NOT NULL ,
    "status" VARCHAR (20)
);

CREATE TABLE roomies
(
    roomie1 INTEGER NOT NULL ,
    roomie2 INTEGER NOT NULL ,
    CONSTRAINT constrain1
        FOREIGN KEY (roomie1)
        REFERENCES users (id)
        ON DELETE CASCADE,
    CONSTRAINT constrain2
        FOREIGN KEY (roomie2)
        REFERENCES users (id)
        ON DELETE CASCADE
);

