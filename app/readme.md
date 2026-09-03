# Microblog

A microblogging web application built with **Flask**, following **Miguel Grinberg's Flask Mega-Tutorial**.

The project follows the tutorial from the initial Flask application through its database, authentication, user relationships, search, internationalization, JavaScript/AJAX functionality, notifications, background jobs, deployment and API concepts.

Tutorial: [The Flask Mega-Tutorial, Part I: Hello, World!](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

# Features

The application includes functionality developed throughout the Flask Mega-Tutorial, including:

* User registration, login and logout
* Password reset through email
* User profiles
* User avatars
* Following and unfollowing users
* Followers and following lists
* Creating and editing posts
* Pagination
* Timestamps and date/time handling
* Internationalization and localization
* Post translation
* AJAX-based functionality
* Full-text search with Elasticsearch
* User notifications
* Database migrations
* Email support
* REST-style API functionality
* Docker-based deployment

## Technologies

### Backend

* Python
* Flask
* SQLAlchemy
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Login
* Flask-Mail
* Flask-WTF

### Database

* MySQL
* SQLAlchemy
* Alembic / Flask-Migrate

### Search

* Elasticsearch

### Translation

* LibreTranslate

### Frontend

* HTML
* Jinja2
* Bootstrap
* JavaScript
* AJAX

### Deployment

* Docker
* Docker Compose
* Gunicorn
* Nginx

## Running the Application

### Local Development

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

The application uses environment variables for configuration. Create a `.env` file containing the required configuration for the database, email, Elasticsearch and LibreTranslate.

Then run the Flask application:

```bash
flask run
```

A different port can be specified when necessary:

```bash
flask run -p 8100
```

## Database Migrations

Database schema changes are managed with Flask-Migrate.

To apply existing migrations:

```bash
flask db upgrade
```

To create a new migration after modifying a database model:

```bash
flask db migrate -m "Describe the change"
```

Then apply it with:

```bash
flask db upgrade
```

## Elasticsearch

Elasticsearch is used to provide full-text search functionality for the application.

The Elasticsearch instance is configured with HTTPS and authentication, with the application using the configured CA certificate to verify the connection.

When Flask runs inside Docker, the application connects to Elasticsearch using the Docker service name.

When Flask runs directly on the host machine, it connects through the published Elasticsearch port.

## Translation

The application uses a locally hosted **LibreTranslate** service for post translation.

The Docker configuration currently loads:

* English
* Spanish
* German

When the Flask application runs inside Docker, LibreTranslate is accessed through the Docker service name:

```text
http://libretranslate:5000
```

When Flask runs directly on the host machine, the published port can be used instead.

## Configuration

The application uses environment variables rather than hard-coding configuration values and credentials.

Configuration includes values for:

```text
SECRET_KEY
DATABASE_URL

MAIL_SERVER
MAIL_PORT
MAIL_USE_TLS
MAIL_USERNAME
MAIL_PASSWORD

ELASTICSEARCH_URL
ELASTICSEARCH_USERNAME
ELASTICSEARCH_PASSWORD
ELASTICSEARCH_CA_CERT

LIBRETRANSLATE_URL
```

The values differ depending on whether the application is running locally or inside Docker.


## Deployment

The application is intended to run in production using:

```text
Internet
   │
   ▼
 Nginx
   │
   ▼
Gunicorn
   │
   ▼
 Flask
   │
   ├── MySQL
   ├── Elasticsearch
   └── LibreTranslate
```

Nginx acts as the reverse proxy in front of the Flask application, while Gunicorn is used as the application server.

## Learning Resource

This project follows **The Flask Mega-Tutorial** by **Miguel Grinberg**.

The tutorial covers the development of the application from the basics of Flask through more advanced topics such as database integration, authentication, search, asynchronous/background functionality, Docker deployment and APIs.

The tutorial series can be found here:

[The Flask Mega-Tutorial, Part I: Hello, World!](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

## Version

Current release:
v1.0.0


This represents the first version of the application being prepared for deployment.

Future changes and additional functionality can be released under subsequent versions.

## Author

**Rikesh Mandal**

Built while following Miguel Grinberg's Flask Mega-Tutorial as a practical project for learning Flask and related web application technologies.
