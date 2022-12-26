INSERT INTO users 
(username, "name", email, password, status) 
VALUES ("mh988", "Abby", "abby@email.com", "78a4071dff4511711044bd45c6ca993fbbc0569cf737eec921c3f1c1f49c25083c8891a206dac6db1561246e96d01f4dda9350ff18068d07a1e1c1f43f3a0a10:020bfe7b111c44069068289a8f5b4e6f", "active");
-- abby12345

INSERT INTO users
(username, "name", email, password, status)
VALUES ("davidwxy","David", "david@email.com", "dc15c24d0febfecf21d0d80f09b2150949505a878a59760f5356c070703b32d9041abefaca2de764ee4015fa46ba95d743f2d1f104a017d69f0da4ffaa6e0db9:bc6e14f7dbf44102b112afc82b0bfe72", "active");
-- david12345

INSERT INTO users
(username, "name", email, password, status)
VALUES ("xxy", "Mie", "mie@email.com", "0cce1e67046bff9271ed1fca85218054c3dd172f01dce6639ef99b9ddc0d31a48a65f3a2f0e027186ca437a50be3f3703df125066393dc499b83ec31297e8628:69f1aa5b281e42cf8d1a67d4fcccc483", "active");
-- mie12345

INSERT INTO users
(username, "name", email, password, status, IP)
VALUES ("wolfwolf", "huiTaiLang", "htl@email.com", "d0a65ea91596ed1643f281d08c3923c2b146455e309e6e6403de19489b4d2f49a4700b094cb8b3932fd39a5392473941c23cbce0cacb81f69dbb081eb7f9ec09:046820e9bc4b4cca86f95d243b1e2553", "active", "0.0.0.0");
-- htl12345

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
