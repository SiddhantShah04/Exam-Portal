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

CREATE TABLE activeStudents(
    id SERIAL NOT NULL PRIMARY KEY,
    examId int REFERENCES EXAM(id),
    roll INT NOT NULL,
    Subject VARCHAR(255) NOT NULL
);

CREATE TABLE QuestionData(
    id SERIAL NOT NULL PRIMARY KEY,
    userId int REFERENCES professor(id),
    Subject TEXT NOT NULL,
    Question TEXT NOT NULL,
    Option1 TEXT NOT NULL,
    Option2 TEXT NOT NULL,
    Option3 TEXT NOT NULL,
    Option4 TEXT NOT NULL,
    Answer TEXT NOT NULL,
    Time INT NOT NULL,
    Image TEXT 
);

CREATE TABLE Result(
    id SERIAL NOT NULL PRIMARY KEY,
    examId INT NOT NULL REFERENCES EXAM(id),
    roll INT NOT NULL,
    Marks INT NOT NULL

)

