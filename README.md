### Create virtual environment

```
$ virtualenv venv -p python3
```

### Activate virtual environment

```
$ source venv/bin/activate
```

### Create PostgreSQL database

```
$ sudo -u postgres psql
    
	>>>  create database drf_functionality;
	>>>  create user postgres;
	>>>  grant all privileges on database drf_functionality to postgres;

```

### Migration command

```
$ python manage.py makemigrations
$ python manage.py migrate
    
```

### Create super admin user

```
$  python manage.py createsuperuser
	>>>  email_address : admin@moweb.com
	>>>  username : Admin
	>>>  password : Admin123!@#
```

### Run django server

```
$ python3 manage.py runserver
```
