INSERT INTO users 
(username, email, password, status) 
VALUES ("Abby", "abby@email.com", "abby12345", "active");

INSERT INTO users
(username, email, password, status)
VALUES ("David", "david@email.com", "david12345", "active");

INSERT INTO users
(username, email, password, status)
VALUES ("Mie", "mie@email.com", "mie12345", "active");

INSERT INTO users
(username, email, password, status)
VALUES ("huiTaiLang", "htl@email.com", "htl12345", "active");

INSERT INTO rooms
(roomname)
VALUES ("sheepVillage");

INSERT INTO roomies
(roomId, roomieId)
VALUES (1, 1);

INSERT INTO roomies
(roomId, roomieId)
VALUES (1, 2);

INSERT INTO requests
(senderId, roomId)
VALUES (3, 1);