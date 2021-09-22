# Pitbull - backend 

### Endpoints:
* (GET) /pitbull/users  -  get all users' data
* (POST) /pitbull/users/  -  create new user  (provide username and password in form-data)
* (DELETE) /pitbull/users/  - delete desired user  (provide username in form-data)

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
