DROP TABLE IF EXISTS professor;

SET search_path = public;

CREATE TABLE professor (
    id SERIAL NOT NULL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

