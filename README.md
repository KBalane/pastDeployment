# DigiInsurance-backend
***

### Installation guide:

```https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/```

### Steps to run:

Create env"
```py -m venv env```

Activate env:
```source env/Scripts/activate```

Install dependencies:
```pip install -r requirements.txt```

Make migrations:
```python manage.py makemigrations```

Migrate:
```python manage.py migrate --run-syncdb && python manage.py migrate```

Run Server:
```python manage.py runserver```

One liner:
```pip install -r requirements.txt && py -m venv env && source env/Scripts/activate && python manage.py makemigrations && python manage.py migrate --run-syncdb && python manage.py migrate && python manage.py runserver```

