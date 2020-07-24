DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS QuestionData;
DROP TABLE IF EXISTS EXAM;

SET search_path = public;

CREATE TABLE professor (
    id SERIAL NOT NULL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

Create TABLE EXAM(
    id SERIAL NOT NULL PRIMARY KEY,
    branch VARCHAR(255) NOT NULL,
    Semester VARCHAR(255) NOT NULL,
    Subject VARCHAR(255) NOT NULL,
    userID INT  NOT NULL,
    status VARCHAR(255) NOT NULL
);

Create TABLE QuestionData(
    id SERIAL NOT NULL PRIMARY KEY,
    userId int REFERENCES professor(id),
    Subject TEXT NOT NULL,
    Question TEXT NOT NULL,
    Options TEXT NOT NULL,
    Answer TEXT NOT NULL,
    Time INT NOT NULL,
    Image TEXT 
);

