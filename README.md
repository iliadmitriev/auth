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

# production

---

## prepare

1. migrate
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
