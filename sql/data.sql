INSERT INTO users 
(username, "name", email, password, status) 
VALUES ("mh988", "Abby", "abby@email.com", "abby12345", "active");

INSERT INTO users
(username, "name", email, password, status)
VALUES ("davidwxy","David", "david@email.com", "david12345", "active");

INSERT INTO users
(username, "name", email, password, status)
VALUES ("xxy", "Mie", "mie@email.com", "mie12345", "active");

INSERT INTO users
(username, "name", email, password, status)
VALUES ("wolfwolf", "huiTaiLang", "htl@email.com", "htl12345", "active");

INSERT INTO rooms
(roomname)
VALUES ("sheepVillage");

INSERT INTO roomies
(roomId, roomieId)
VALUES (1, 1);

INSERT INTO roomies
(roomId, roomieId)
VALUES (1, 2);

INSERT INTO roomies
(roomId, roomieId)
VALUES (1, 3);

INSERT INTO requests
(senderId, roomId)
VALUES (3, 1);