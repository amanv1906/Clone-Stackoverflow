# Capstone Project - Stackoverflow clone

This project is a simplified a full stack clone of Stackoverflow. Front-End code is in ReactJS Which is taken fron Open source github project. We have worked on Server(Api Development) Part using Django Rest Framework.

# Source Project
The original frontend is taken from open source project.

* https://github.com/salihozdemir/stackoverflow-clone

# Tech Stack 
* React Js
* Django Rest Framework
* Postgresql

# To Run App in local machine

## To Run App Using Docker Container

1. Clone repository
```bash
    $ git clone https://gitlab.com/mountblue/cohort-14-python/capstone-team1.git
```
2. To Build the image
```bash
    $ sudo docker-compose build
```
3. To Run the container
```bash
    $ sudo docker-compose up
```
4. To create super user for admin
```bash
    docker exec -it conatiner_id python manage.py createsuperuser
```
5. To open App on Browser Visit

    Front End URL : http://localhost:3000/

    Back-End Admin: http://127.0.0.1:8000/admin/

5. To destroy the container with data
```bash
    $ sudo docker-compose down -v
```

## To Run App in Local Machine Without Docker


### First run client server
1. Clone repository
```bash
    git clone https://gitlab.com/mountblue/cohort-14-python/capstone-team1.git
```
2. Change directory into client
```bash
    cd ../client
```
3. Install all dependencies
```bash
    npm install
```
4. To run cliet on local
```bash
    npm run dev
```
5. Open Clinet App on Browser 
   
   http://localhost:3000/


### To create the Database

1. Change directory to server

2. Run the postgres server by:  
```bash
   sudo -u postgres psql
```
3. To Create the database 
```bash
    \i create-helper.sql
```
4. To drop the database
```bash
    \i drop-helper.sql
```

### To Run Server in local

1. Install all dependency - inside server directory   
```bash
    pip install -r requirements.txt
```
2. Migrate the models
```bash
    pyhton manage.py migrate
```
3. To create super user or admin user
```bash
    python manage.py createsupeuser
```
4. To run server
```bash
    pyhton manage.py runserver
```
5. To visit Admin on browser

    Admin URL : http://127.0.0.1:8000/admin


# To Browse App on Cloud

App is deployed on Linode server

Front End URL : http://192.46.210.128:3001/

Back-End Admin: http://192.46.210.128:8000/admin/


# API Listing

#### BASE URL - http://127.0.0.1:8000/api

#### Authentication API

* `post /signup`
* `post /authenticate`     

#### Users API

* `get  /users`
* `get  /users/:search`
* `get  /user/:username`

#### Questions API

* `post  /questions`
* `get  /question/:question`
* `get /question`
* `get /question/:tags`
* `get /question/user/:username`
* `delete /question/:question`

#### Tags API

* `get /tags/populertags`
* `get /tags/:tag`
* `get /tags`

#### Answers API

* `post /answer/:question`
* `delete /answer/:question/:answer`

#### Votes API

* `get /votes/upvote/:question/:answer?`
* `get /votes/downvote/:question/:answer?`
* `get /votes/unvote/:question/:answer?`

#### Comments API

* `post /comment/:question/:answer?`
* `delete /comment/:question/:comment`
* `delete /comment/:question/:answer/:comment`
