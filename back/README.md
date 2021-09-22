# Pitbull - backend 

### Endpoints:
* (GET) /pitbull/users  -  get all users' data
* (POST) /pitbull/users/  -  create new user  (provide username and password in form-data)
* (DELETE) /pitbull/users/  - delete desired user  (provide username in form-data)
* (POST) /pitbull/users/superuser/  - create superuser account (provide username and password in form-data)
* (GET) /pitbull/users/current - get username of currently logged-in user
* (POST) /pitbull/login/  - login user (provide username and password in form-data)
* (POST) /pitbull/logout/  - logout current user

## Running development server
```
python manage.py runserver [port or address:port]
```
## Creating migrations
```
python manage.py makemigrations
```
## Running migrations
```
python manage.py migrate
```
