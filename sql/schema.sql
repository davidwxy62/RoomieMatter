PRAGMA foreign_keys = ON;

CREATE TABLE users
(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(40) NOT NULL UNIQUE,
    "password" VARCHAR (256) NOT NULL ,
    "status" VARCHAR (20)
);

CREATE TABLE rooms
(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    roomname VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE roomies
(
    roomId INTEGER NOT NULL,
    roomieId INTEGER NOT NULL UNIQUE,
    CONSTRAINT room_fk
        FOREIGN KEY (roomId)
        REFERENCES  rooms (id)
        ON DELETE CASCADE,
    CONSTRAINT roomie_fk
        FOREIGN KEY (roomieId)
        REFERENCES  users (id)
        ON DELETE CASCADE
);

CREATE TABLE requests
(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    senderId INTEGER NOT NULL,
    roomId INTEGER NOT NULL,
    CONSTRAINT unique_pair
        UNIQUE (senderId, roomId),
    CONSTRAINT sender_fk
        FOREIGN KEY (senderId)
        REFERENCES  users (id)
        ON DELETE CASCADE,
    CONSTRAINT room_fk
        FOREIGN KEY (roomId)
        REFERENCES  rooms (id)
        ON DELETE CASCADE
);
