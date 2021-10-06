Technology Stack
---

    Python 3.8
    Django 3.2.7
    sqllitedb
    djangorestframework 3.12.4

Running Project
----

Create a virtualenv

```shell
$virtualenv venv
```

Activate the environment

```shell
$source venv/bin/activate
```

Install dependencies

```shell
$pip install -r requirements.txt
```

Go to project directory

* migrate database

```
python manage.py migrate
 ```

Run local server

```shell
python manage.py runserver
```

Created superuser

```shell
python manage.py createsuperuser
```

<hr>
To initialize customer wallet obtain token of superuser 
using obtain token api <br>
  * use obtained token in header to initialize custom wallet
  

