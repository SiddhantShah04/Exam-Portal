DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS QuestionData;

SET search_path = public;

CREATE TABLE professor (
    id SERIAL NOT NULL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

Create TABLE QuestionData(
    id SERIAL NOT NULL PRIMARY KEY,
    Subject TEXT NOT NULL,
    Question TEXT NOT NULL,
    Options TEXT NOT NULL,
    Answer TEXT NOT NULL,
    Time INT NOT NULL,
    Image TEXT 
);


