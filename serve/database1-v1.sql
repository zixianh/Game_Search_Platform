DROP TABLE IF EXISTS `table_favourite1`;
DROP TABLE IF EXISTS `table_user1`;
DROP TABLE IF EXISTS `table_game1`;

CREATE TABLE `table_game1` (
  `gameid` VARCHAR(11) NOT NULL,
  `gamename` VARCHAR(100) DEFAULT NULL,
  `gametag` VARCHAR(130) DEFAULT NULL,
  `gameplatform` VARCHAR(30) DEFAULT NULL,
  `favorablerate` FLOAT DEFAULT NULL,
  `price` FLOAT DEFAULT NULL,
  PRIMARY KEY (`gameid`)
);

CREATE TABLE `table_user1` (
  `user_id` VARCHAR(4) NOT NULL,
  `user_name` VARCHAR(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
);

CREATE TABLE table_favourite1 (
  user_id VARCHAR(4),
  gameid VARCHAR(11),
  username VARCHAR(255),
  PRIMARY KEY (user_id, gameid),
  FOREIGN KEY (user_id) REFERENCES table_user1(user_id) ON DELETE CASCADE,
  FOREIGN KEY (gameid) REFERENCES table_game1(gameid) ON DELETE CASCADE
);