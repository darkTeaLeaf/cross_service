# cross_service
Cross-Service is a web-platform that allows users to post their services and requests. 
Software project by BS17-07-04 group

## install requirements
For using this project you are required to <a href="https://docs.djangoproject.com/en/2.2/topics/install/">install django</a>

## DB organisation
![alt text](https://github.com/darkTeaLeaf/cross_service/blob/master/db.png)

## Run the project
First of all, you will need to build sqlite3 database: 
<code> python3 manage.py migrate | python3 manage.py makemigrations </code>. <br>
Secondly, it is up to you to customise settings via **manage.py** command. Try
<code> python3 manage.py help </code> to see all possible commands. <br>

Basically, you will need only commands as follows: 
```
createsuperuser -- create new admin
runserver       -- run the project
```


