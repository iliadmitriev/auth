# install

---

1. install python3 and create virtual env
```shell
python3 -m venv venv
source venv/bin/activate
```
2. install requirements
```shell
pip install -r requirements.txt
```
3. generate new django secret key and put it into file .env
```shell
echo DJANGO_SECRET_KEY=\'$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')\'  >> .env
```
4. export variables from .env file
```shell
export $(cat .env | xargs)
```
5. create a db (run migrations)
```shell
python3 manage.py migrate
```
6. compile messages
```shell
python3 manage.py compilemessages
```
7. create superuser
```shell
python3 manage.py createsuperuser
```

# development

---
1. set environment variables
```shell
DJANGO_DEBUG=True
```

2. make migrations and migrate
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

3. make messages
```shell
python3 manage.py makemessages -a
python3 manage.py compilemessages
```

4. run
```shell
python3 manage.py runserver 0:8000
```

# testing

## run tests 

1. run all tests
```shell
python3 manage.py test
```
2. run with keeping db in case of test fails
```shell
python3 manage.py test --keepdb
```
3. run all tests with details
```shell
python3 manage.py test --verbosity=2
```
⚠️ parallel test running doesn't work under Windows and macOS

## run tests with coverage

1. install coverage
```shell
pip install coverage
```
2. run with coverage
```shell
coverage run --source='.' manage.py test
```
3. print report with missing lines
```shell
coverage report -m
```
4. generate detailed html report
```shell
coverage html
open htmlcov/index.html
```
⚠️ coverage doesn't work when running test parallel under Windows and macOS


# how to use

1. register new account
```shell
curl -v -H 'Accept: application/json; indent=4' \
  -H 'Content-Type: application/json' \
  -d '
    {
        "email": "youremailbox@example.com",
        "password": "yourpassword",
        "password2": "yourpassword"
    }' \
    http://localhost:8000/auth/register/
```
2. get auth token
```shell
curl -v -H 'Accept: application/json; indent=4' \
  -H 'Content-Type: application/json' \
  -d '
    {
        "username": "youremailbox@example.com",
        "password": "yourpassword"
    }' \
    http://localhost:8000/auth/token/
```
3. get restricted data using auth tocken
```shell
curl -v -H 'Accept: application/json; indent=4' \
  -H 'Authorization: Bearer youraccessotoken' \
  http://localhost:8000/auth/user/
```
4. refresh token
```shell
curl -v -H 'Accept: application/json; indent=4' \
  -H 'Content-Type: application/json' \
  -d '
  {
    "refresh": "your refresh token goes here"
  }' \
  http://localhost:8000/auth/token/refresh/
```
⚠️ by default token is expiring in 5 minutes, after that you will get message `Token is invalid or expired` with `403 Forbidden` http code


# production

---

## prepare

1. migrate migrations
```shell
python3 manage.py migrate --noinput
```
2. collect static
```shell
python3 manage.py collectstatic --noinput
```

3. compile messages
```shell
python3 manage.py compilemessages
```

## Web server

### uWSGI

1. install uWSGI
```shell
pip install uWSGI
```

2. Run
```shell
uwsgi --ini uwsgi.ini
```

## Docker

### Build image

1. create .env file with environment variables
```shell
DJANGO_SECRET_KEY='hr=2w^5-!vr0pv=2mjw^$g-*&=9=j%a_zwg5h1cq21inisqmd'
POSTGRES_HOST=auth.idm.dev
POSTGRES_PORT=5432
POSTGRES_DB=auth
POSTGRES_USER=auth
POSTGRES_PASSWORD=kO5sA8iB0cC3hH0a
MEMCACHED_LOCATION=auth.idm.dev:11211
```
2. build docker image
```shell
docker build -t auth ./
```
3. create postgres instance
```shell
docker run -d -p 5432:5432 --name auth-postgres --env-file .env postgres:13.2-alpine
```
4. create memcached instance
```shell
docker run -d -p 11211:11211 --name auth-memcached --env-file .env memcached:alpine
```
5. create auth instance
```shell
docker run -d -p 8000:8000 --name auth-api --env-file .env auth
```
6. run migrations
```shell
docker exec -ti auth-api python3 manage.py migrate
```
7. create super user
```shell
docker exec -ti auth-api pyt hon3 manage.py createsuperuser
```