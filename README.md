# Django REST API for sending email messages

Rest api build with Django Rest Framework. Api allows to send multiple emails. Main features:
<ul>
<li>sending emails to any addresses (using Celery)</li>
<li>using previously defined messages and topics (Template model)</li>
<li>using previously defined mailbox (Mailbox model)</li>

</ul>

## Used technologies

<ul>
<li>Python</li>
<li>Django, Django Rest Framework (DRF)</li>
<li>PostgreSQL</li>
<li>Celery</li>
<li>django-filter</li>
<li>django-environ</li>
</ul>


### Installing

To install and run this project you must have to install Redis message broker and PostgreSQL db.

<ol>
<li>Install Redis and PostgresSQL</li>
<li>Configure new database and db user, then fire up db and redis services</li>
<li>Create .env file, put it into project root folder(right next to requirements.txt file), fill it with your configuration:

```
# Django conf
SECRET_KEY=
DEBUG=on

# PostgreSQL conf
POSTGRES_NAME=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=

# Celery conf
BROKER_URL=
CELERY_RESULT_BACKEND=
```
</li>
<li>Create virtual environment and install requirements from requirements.txt file</li>
<li>Go to email_api/email_api and run Celery worker (with activated venv)

```
celery -A email_api worker -l info
```
</li>
<li>Fire up Django server:

```
python manage.py runserver
```
</li>
</ol>



### Testing app

Now you can open web broswer and hit url:  
http://localhost:8000/api/

Available api endpoints:  
  

| HTTP method              	| url       	        | available actions  	                    |
| -------------------------	| -------------------	| -----------------------------------------	|
| GET, POST               	| api/mailbox       	| show all mailboxes, create new mailbox  	|
| GET, PUT, PATCH, DELETE 	| api/mailbox/:id/  	| show, update or delete single mailbox   	|
| GET, POST               	| api/template/     	| show all templates, create new template 	|
| GET, PUT, PATCH, DELETE 	| api/template/:id/ 	| show, update or delete single template  	|
| GET, POST               	| api/email/        	| show emails, send new one               	|
