-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS part;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- a new parts table is created for each user, the schema looks like this
-- CREATE TABLE part (
--  `id` int(6) NOT NULL DEFAULT '0',
--  `type` char(50) NOT NULL,
--  `class` int(8) NOT NULL DEFAULT '-1',
--  `qty` int(5) NOT NULL,
--  `pkg` char(7) NOT NULL,
--  `manuf` char(25) DEFAULT NULL,
--  `partnum` char(25) DEFAULT NULL,
--  `cost` char(25) DEFAULT NULL,
--  `location` char(25) NOT NULL,
--  `description` varchar(255) NOT NULL,
--  `notes` varchar(255) DEFAULT NULL,
--  `url` varchar(255) NOT NULL,
--  PRIMARY KEY (`id`)
--);

-- old blog post schema from flaskr example
--CREATE TABLE post (
--  id INTEGER PRIMARY KEY AUTOINCREMENT,
--  author_id INTEGER NOT NULL,
--  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--  title TEXT NOT NULL,
--  body TEXT NOT NULL,
--  FOREIGN KEY (author_id) REFERENCES user (id)
--);
