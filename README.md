# Online Examination Portal
![index](https://user-images.githubusercontent.com/42845723/92633049-d9004300-f2ef-11ea-98c8-146b4e4da143.png)

**Online Examination portal** is a web-based application for multiple-choice question (MCQ) based exam. The purpose of portal is to take online test in an efficient manner and no wastage of time for checking the paper. 

The main objective of the portal  is to effectively evaluate the candidate thoroughly through a fully automated system that not only saves lot of time but also gives fast results.


## Table of Contents

1. [Technologies](#technologies)
2. [Features](#features)
3. [Installation](#installation)
  
## <a name="technologies"></a>Technologies

**Front-end:** [HTML5](http://www.w3schools.com/html/), [CSS](http://www.w3schools.com/css/),[Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [jQuery](https://jquery.com/), [AJAX](http://api.jquery.com/jquery.ajax/)
**Back-end:** [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/), [Jinja2](http://jinja.pocoo.org/docs/dev/), [PostgreSQL](http://www.postgresql.org/), [SQLAlchemy](http://www.sqlalchemy.org/)

## <a name="features"></a>Features
## Professor module
- After you Logged In ,Click on Download CSV format and inside of the file you can type questions , option , time and answers.
- At last click on Deactivate to activate the exam of the following subject.


![index](https://user-images.githubusercontent.com/42845723/93713929-c0f4b300-fb7c-11ea-9b98-c81c5284e300.png)


- Add image to question if you want to, by clicking on edit option.

![editNew](https://user-images.githubusercontent.com/42845723/93714451-56457680-fb80-11ea-8f11-b8b2bda68ffe.PNG)

- Questions , options , answers and time in seconds all are uploaded to the website in a CSV file.

![upload](https://user-images.githubusercontent.com/42845723/93714484-97d62180-fb80-11ea-9206-6fcd88aa1275.png)


- Generate result in real time.
![result](https://user-images.githubusercontent.com/42845723/93714504-c0f6b200-fb80-11ea-9da5-e70250ce1d1e.png)

## Student module
- Test page include Timer, Roll number of student, current and total number of questions and Submit button.
- The questions are selected at **random with shuffle options** from questions uploaded.

![questionimage](https://user-images.githubusercontent.com/42845723/93714752-5a729380-fb82-11ea-8066-5521b1e68203.png)


## <a name="installation"></a>Features
## Installation
Install [PostgreSQL](http://postgresapp.com).

Postgres needs to be running in order for the app to work. It is running when you see the elephant icon:

### Set up ExamPortal:

Clone this repository:

```$ git clone https://github.com/sidd044/Exam-Portal```



Install the dependencies:

```$ pip install -r requirements.txt```

you need to tell your terminal the application to work with by setting the FLASK_APP environment variable.

```$ set FLASK_APP=flaskr```

Run PostgreSQL .

Create database with the name `examportal`.

```$ flaskr init-db```

Go to `localhost:5000` in your browser to start using ExamPortal!
