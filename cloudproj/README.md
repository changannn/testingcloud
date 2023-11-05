## Installing Django
1. Ensure python is installed
```
python --version (windows)
python3 --version (mac)
```
2. Use python's package manager pip to install django
```
pip install django
```
3. Clone the repository into desired directory
```
git clone https://github.com/yyueda/cloudproj
```
4. CD into cloudproj directory
5. Migrate the migrations to your database (change your password and username in the settings.py)
```
python manage.py migrate (windows)
python3 manage.py migrate (mac)
```
6. Run the server on http://127.0.0.1:8000/
```
python manage.py runserver (windows)
python3 manage.py runserver (mac)
```

## Migrating to the database

Ensure you have mysql server/workbench downloaded and that your settings in settings.py matches to your personal configurations.
After any changes to the model. Run `python manage.py makemigrations` to create migrations. Run `python manage.py migrate` to migrate to the database.
If you have an error with mysqlclient, run `pip install mysqlclient` which is a MySQL database connector for python.

## Creating another app in the django project

Run `python manage.py startapp APPNAME` to create a separate app in the project.

## Populating the Database
You can populate the database with initial data using the provided db.json file. Follow these steps:
1. Ensure that your database is properly configured in the settings.py file.
2. Run the following command to load the initial data from db.json into your database: `python manage.py loaddata db.json`

## Running the server
Run `python manage.py runserver` to run the server on http://127.0.0.1:8000/.

## Further help

To get more help on Django, please check out the [Django Documentation Page](https://docs.djangoproject.com/en/4.2/).
