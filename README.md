# Cross Service
This is a web-platform that allows users to post their services and requests.

>This project is built for IU SWP course by BS2-7-4.

## Requirements
To use this project, you are required to <a href="https://docs.djangoproject.com/en/2.2/topics/install/">install Django</a>.

## Database organisation
![alt text](https://github.com/darkTeaLeaf/cross_service/blob/master/db.png)

## Run the project
Firstly, you will need to build SQlite3 database: 
<code> python3 manage.py migrate | python3 manage.py makemigrations </code>. <br>
Secondly, it is up to you to customise settings via manage.py. Try
<code> python3 manage.py help </code> to see all possible commands. <br>

Basically, you will need only the following commands to demo the project: 
```
createsuperuser -- create new admin
runserver       -- run the project
```
