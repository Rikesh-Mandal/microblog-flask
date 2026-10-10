# Microblog

A full-stack microblogging web application built with **Flask**, following **Miguel Grinberg's Flask Mega-Tutorial** as its primary learning resource.

The project progresses from the core Flask application through database integration, authentication, user relationships, search, internationalization, JavaScript/AJAX functionality, notifications, Docker-based infrastructure, REST API development, API documentation and cloud deployment.

The project has also been extended with a multi-service Docker Compose environment, MySQL persistence, Elasticsearch with authenticated HTTPS connections, locally hosted LibreTranslate, REST API endpoints and OpenAPI documentation.

**Tutorial:** [The Flask Mega-Tutorial, Part I: Hello, World!](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

---

## Live Project

* **Live Application:** [View the deployed Microblog application](https://microblog-flask-production.up.railway.app/)
* **API Documentation:** [View the OpenAPI documentation](https://rikesh-mandal.github.io/microblog-flask/)

The REST API is documented using **OpenAPI 3.0** and rendered with **Scalar**.

The documentation covers users, posts, messages, authentication, pagination, request bodies, response schemas and error responses.

---

## Features

### User Management

* User registration
* Login and logout
* Password hashing
* Password reset through email
* User profiles
* User avatars
* Last-seen tracking
* Profile editing

### Social Features

* Follow and unfollow users
* Followers list
* Following list
* User-specific post feeds
* User notifications

### Posts

* Create posts
* Edit posts
* Delete posts through the REST API
* Post timestamps
* Updated timestamps
* Pagination
* Full-text search with Elasticsearch
* Post translation using LibreTranslate

### Frontend

* Server-rendered pages using Jinja2
* Bootstrap-based interface
* JavaScript and AJAX functionality
* Dynamic user interactions
* Notification polling and client-side functionality

### REST API

The application includes REST-style API endpoints for:

* Users
* Posts
* Followers
* Following
* Messages
* Authentication tokens

The API includes:

* HTTP Basic Authentication for obtaining API tokens
* Bearer token authentication for protected endpoints
* Pagination
* JSON request and response handling
* HTTP status codes
* Error responses
* Resource URLs through `Location` headers
* OpenAPI 3.0 documentation

---

## Technology Stack

### Backend

* Python
* Flask
* SQLAlchemy
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Login
* Flask-Mail
* Flask-WTF
* Flask-HTTPAuth
* Gunicorn

### Database

* MySQL
* SQLAlchemy ORM
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

### API

* REST
* HTTP Basic Authentication
* Bearer Token Authentication
* OpenAPI 3.0
* Scalar API Documentation

### Infrastructure & Deployment

* Docker
* Docker Compose
* Docker named volumes
* Docker service networking
* Environment-based configuration
* Gunicorn
* Railway
* GitHub Pages

---

## Architecture

The project has two main environments:

1. A **local/containerized environment** containing the full supporting service stack.
2. A **Railway production deployment** containing the core application and MySQL database.

### Local Docker Architecture

The local environment uses Docker Compose to run multiple services together.
```text

                      Docker Compose Network
                              │
          ┌───────────────────┼───────────────────┬───────────────────┐
          │                   │                   │                   │
          ▼                   ▼                   ▼                   ▼
     Flask App              MySQL           Elasticsearch      LibreTranslate
     + Gunicorn            Database             Search           Translation
                              │                   │
                              ▼                   ▼
                         mysql-data        elasticsearch-data
                           volume               volume
```

The services communicate over Docker's internal network using their service names rather than relying on hard-coded IP addresses.

For example:

```text
Flask
  │
  ├── mysql
  │     └── relational database
  │
  ├── elasticsearch
  │     └── full-text search
  │
  └── libretranslate
        └── post translation
```

This allows the services to be started and managed together while remaining independently containerized.

---

## Docker and Docker Compose

The project includes a Docker-based environment for running the Flask application and its supporting infrastructure.

The application container is built from a Python base image and includes the application source code, dependencies, migrations and Gunicorn.

The supporting Docker Compose services include:

* Flask application
* MySQL
* Elasticsearch
* LibreTranslate

The environment demonstrates several Docker concepts beyond simply containerizing the Flask application:

* Multi-container orchestration with Docker Compose
* Internal Docker networking
* Service discovery using Compose service names
* Environment-variable configuration
* Persistent named volumes
* Port publishing
* Database persistence
* Elasticsearch persistence
* Containerized external services
* Application startup through a container entrypoint script

The environment can be started using:

```bash
docker compose up
```

To rebuild application images after dependency or Dockerfile changes:

```bash
docker compose up --build
```

To stop the environment:

```bash
docker compose down
```

Named volumes are intentionally kept when using `docker compose down`, allowing persistent service data to survive container recreation.

---

## Persistent Storage

Docker named volumes are used for services where data should survive container deletion and recreation.

### MySQL

MySQL data is stored in a persistent volume mounted at:

```text
/var/lib/mysql
```

Conceptually:

```text
mysql-data
    │
    ▼
/var/lib/mysql
```

This means recreating the MySQL container does not automatically delete the application's database.

### Elasticsearch

Elasticsearch data is similarly persisted using a named volume mounted at:

```text
/usr/share/elasticsearch/data
```

Conceptually:

```text
elasticsearch-data
        │
        ▼
/usr/share/elasticsearch/data
```

If Elasticsearch is intentionally recreated with a clean index, application data can be indexed again from the relational database.

---

## Database

The application uses **MySQL** as its relational database.

SQLAlchemy provides the ORM layer while Flask-Migrate and Alembic manage schema migrations.

The application supports environment-based database URLs, allowing the connection configuration to change between local development, Docker and Railway without changing application code.

Within Docker Compose, the Flask application communicates with MySQL through the internal Docker network.

The database is also backed by a Docker named volume to maintain persistence across container recreation.

---

## Database Migrations

Database schema changes are managed using Flask-Migrate and Alembic.

To apply existing migrations:

```bash
flask db upgrade
```

After changing a SQLAlchemy model, generate a new migration with:

```bash
flask db migrate -m "Describe the change"
```

Then apply it:

```bash
flask db upgrade
```

Useful migration commands also include:

```bash
flask db current
```

and:

```bash
flask db history
```

---

## Elasticsearch

Elasticsearch provides full-text search functionality for posts.

The local Docker environment runs Elasticsearch as its own service.

The Elasticsearch instance uses authentication and HTTPS. The Flask application connects using configuration supplied through environment variables.

Configuration includes:

```text
ELASTICSEARCH_URL
ELASTICSEARCH_USERNAME
ELASTICSEARCH_PASSWORD
ELASTICSEARCH_CA_CERT
```

A CA certificate is made available to the Flask application so that it can verify the Elasticsearch HTTPS connection.

When running inside Docker, the Flask application reaches Elasticsearch through its Docker service name.

If an Elasticsearch index is recreated or a clean Elasticsearch volume is used, application records can be indexed again from the database.

---

## LibreTranslate

Post translation is supported using a locally hosted **LibreTranslate** service.

LibreTranslate runs as a separate service in the Docker environment rather than relying on an externally hosted translation API.

The local configuration includes language support for:

* English
* Spanish
* German

Within the Docker Compose network, the Flask application can communicate with the translation service using its service name:

```text
http://libretranslate:5000
```

When the Flask application runs directly on the host instead of inside Docker, the published LibreTranslate port can be used instead.

Because LibreTranslate and its language models require considerably more storage than the core Flask application, LibreTranslate is currently used as a local/self-hosted service rather than part of the public Railway deployment.

---

## REST API

The application provides REST-style endpoints for working with users, posts, messages and authentication.

Examples include:

```text
GET    /api/users
POST   /api/users
GET    /api/users/{id}
PUT    /api/users/{id}

GET    /api/users/{id}/followers
GET    /api/users/{id}/following
GET    /api/users/{user_id}/posts

GET    /api/posts
POST   /api/posts
GET    /api/posts/{id}
PUT    /api/posts/{id}
DELETE /api/posts/{id}

GET    /api/messages/sent
GET    /api/messages/received

POST   /api/tokens
DELETE /api/tokens
```

Collection endpoints support pagination through query parameters:

```text
?page=1&per_page=10
```

Paginated responses contain:

```json
{
  "items": [],
  "_meta": {
    "page": 1,
    "per_page": 10,
    "total_pages": 1,
    "total_items": 0
  },
  "_links": {
    "self": "...",
    "next": null,
    "prev": null
  }
}
```

---

## API Authentication

The API uses two authentication mechanisms.

### HTTP Basic Authentication

A username and password are supplied to:

```text
POST /api/tokens
```

If the credentials are valid, the endpoint returns an authentication token.

### Bearer Token Authentication

The returned token is then supplied to protected endpoints using:

```text
Authorization: Bearer <token>
```

The token can be revoked using:

```text
DELETE /api/tokens
```

---

## API Documentation

The API is documented using the **OpenAPI 3.0 specification**.

The source specification is stored at:

```text
docs/openapi.yaml
```

It documents:

* API paths
* HTTP methods
* Path parameters
* Query parameters
* Request bodies
* Response schemas
* Pagination
* Error responses
* Basic Authentication
* Bearer Token Authentication
* Reusable component schemas

The OpenAPI specification is rendered using **Scalar** and published through **GitHub Pages**.

**Public API Documentation:**

[View the Microblog API Documentation](https://rikesh-mandal.github.io/microblog-flask/)

The API can also be imported into Scalar Desktop for interactive testing.

---

## Configuration

The application uses environment variables rather than hard-coded credentials or service configuration.

Configuration includes values such as:

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

Values can differ depending on whether the application is running:

* Directly on the host
* Inside Docker
* On Railway

Sensitive values should be stored in environment variables and should not be committed to source control.

---

## Running the Application

### Local Python Environment

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

Create a `.env` file containing the required application configuration.

Then run:

```bash
flask run
```

A different port can be specified when necessary:

```bash
flask run -p 8100
```

---

## Docker and Containerized Infrastructure

The project includes a multi-service Docker Compose environment for running the Flask application together with its supporting services.

```text
                         Docker Compose Network
                                  │
          ┌───────────────────────┼───────────────────────┬───────────────────────┐
          │                       │                       │                       │
          ▼                       ▼                       ▼                       ▼
     Flask App                  MySQL               Elasticsearch          LibreTranslate
     + Gunicorn               Database                  Search               Translation
                                  │                       │
                                  ▼                       ▼
                             mysql-data          elasticsearch-data
                                volume                  volume
```

The Flask application image is built locally from the project's `Dockerfile`.

The remaining services use container images pulled from their respective registries:

```text
Flask application   → built from local Dockerfile
MySQL               → MySQL container image
Elasticsearch       → Elastic container registry
LibreTranslate      → LibreTranslate container image
```

All services communicate through the Docker Compose network using service names instead of hard-coded container IP addresses.

For example:

```text
mysql:3306
elasticsearch:9200
libretranslate:5000
```

### Building and Starting the Environment

The complete development environment can be built and started with:

```bash
docker compose up --build
```

Docker Compose will:

* Build the Flask application image from the local `Dockerfile`
* Pull the required third-party service images
* Create the internal Compose network
* Start the Flask, MySQL, Elasticsearch and LibreTranslate services
* Attach the configured persistent volumes
* Make configured ports available to the host

Running services can be viewed with:

```bash
docker compose ps
```

The environment can be stopped with:

```bash
docker compose down
```

Named volumes remain available after containers are stopped or recreated.

---

## Environment Configuration

Application configuration is supplied through environment variables rather than being hard-coded into the source code.

A local `.env` file can be created from the supplied example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

The `.env.example` file contains variable names and example configuration only.

The real `.env` file may contain credentials and secrets and must not be committed to source control.

---

## Persistent Storage

Stateful services require persistent storage so that data survives container recreation.

### MySQL

The Docker environment stores MySQL data under:

```text
/var/lib/mysql
```

using a named Docker volume.

The current development Compose configuration uses an externally managed volume:

```yaml
volumes:
  mysql-data:
    external: true
```

This means Docker Compose expects the volume to already exist.

It can be created manually with:

```bash
docker volume create mysql-data
```

This approach was used during development to protect an existing database volume from accidental recreation.

For a portable development environment, the external requirement can instead be removed:

```yaml
volumes:
  mysql-data:
```

Docker Compose will then create and manage the named volume automatically.

A normal:

```bash
docker compose down
```

does not remove the volume.

Removing persistent data requires an explicit operation such as:

```bash
docker compose down -v
```

and should therefore be used carefully.

### Production Database Storage

A production deployment would normally avoid depending on an unmanaged Docker volume for the primary relational database.

Instead, the application should use either:

```text
Managed MySQL service
        │
        └── provider-managed persistence, backups and recovery
```

or a deliberately provisioned persistent production volume with its lifecycle managed separately from the application containers.

The current Railway deployment follows the managed-service approach, with MySQL running separately from the Flask application.

This prevents application container replacement from affecting persistent database data.

---

## Elasticsearch Persistence

Elasticsearch stores its index data in:

```text
/usr/share/elasticsearch/data
```

The Compose environment uses a named volume:

```yaml
elasticsearch-data:
```

which is mounted into the Elasticsearch container.

Because Elasticsearch is used as a search index rather than the application's primary source of truth, the index can be rebuilt from data stored in MySQL when necessary.

Persistent storage still avoids unnecessary reindexing whenever containers are restarted or recreated.

---

## LibreTranslate Models

LibreTranslate stores downloaded language models in a named volume:

```yaml
libretranslate-models:
```

mounted at:

```text
/home/libretranslate/.local
```

This prevents language models from being downloaded again whenever the LibreTranslate container is recreated.

---

## TLS and Elasticsearch Security

The local Elasticsearch environment uses HTTPS and authentication.

Elasticsearch is configured with:

```text
CA certificate
Server certificate
Server private key
```

The Flask application uses the CA certificate to verify that it is communicating with the expected Elasticsearch service.

Conceptually:

```text
Flask
  │
  │ HTTPS
  │ verifies certificate using CA
  ▼
Elasticsearch
  │
  ├── elasticsearch.crt
  └── elasticsearch.key
```

For local development, certificates can be mounted into containers as read-only files.

For example:

```yaml
volumes:
  - ./certs:/usr/share/elasticsearch/config/certs:ro
```

and the Flask application can receive the CA certificate separately:

```yaml
volumes:
  - ./certs/ca.crt:/certs/ca.crt:ro
```

### Production TLS Handling

Production private keys must not be committed to Git.

Files such as:

```text
elasticsearch.key
```

must be treated as secrets.

A production deployment should obtain certificates and private keys through mechanisms such as:

```text
Cloud/platform secret storage
Container orchestration secrets
Mounted secret volumes
A certificate-management system
Managed Elasticsearch configuration
```

The repository should contain configuration describing where certificates are expected, but not the production private keys themselves.

A CA certificate used only for verification is generally not confidential in the same way as a private key, but it should still be managed deliberately so that the application trusts the correct certificate authority.

Production secret material should be injected when the application is deployed.

For example:

```text
Git repository
     │
     │ contains no private keys
     ▼
Deployment platform
     │
     ├── environment secrets
     ├── TLS certificates
     └── private keys
              │
              ▼
          Containers
```

If TLS for the public application is terminated by a hosting platform or reverse proxy, that platform manages the public HTTPS certificate separately from internal Elasticsearch TLS.

---

## Development vs Production

The complete local Docker environment is:

```text
Flask + Gunicorn
MySQL
Elasticsearch
LibreTranslate
```

The current public Railway deployment is:

```text
Internet
   │
   ▼
Railway
   │
   ▼
Gunicorn
   │
   ▼
Flask
   │
   ▼
Managed MySQL
```

Elasticsearch and LibreTranslate remain supported local/self-hosted services because of their additional memory and storage requirements.

A larger production deployment could run them as dedicated services while keeping application containers stateless and storing credentials, certificates and persistent data outside the application image.


---

## Production Deployment

The public application is deployed using **Railway**.

The current production architecture focuses on the core application:

```text
Internet
   │
   ▼
Railway
   │
   ▼
Gunicorn
   │
   ▼
Flask
   │
   ▼
MySQL
```

Railway hosts the Flask application and MySQL database.

The application is deployed from the GitHub repository and configured using Railway environment variables.

**Production application:**

https://microblog-flask-production.up.railway.app/

### Local vs Production Services

The full local Docker environment contains:

```text
Flask
MySQL
Elasticsearch
LibreTranslate
```

The current Railway deployment contains:

```text
Flask
MySQL
```

Elasticsearch and LibreTranslate were tested as separate deployment services, but their resource requirements exceeded the limits suitable for the current Railway setup.

They therefore remain supported local/self-hosted components rather than being presented as active production services.

---


## Development Workflow

The project is version controlled using Git and hosted on GitHub.

A typical workflow is:

```text
Make changes
    │
    ▼
git status
    │
    ▼
git add
    │
    ▼
git commit
    │
    ▼
git push
    │
    ▼
GitHub
    │
    ├── Source repository
    ├── GitHub Pages API documentation
    │
    └── Railway deployment
```

---

## Learning Resource

This project follows **The Flask Mega-Tutorial** by **Miguel Grinberg**.

The tutorial provided the foundation for learning and implementing Flask concepts including:

* Application structure
* Templates
* Forms
* Authentication
* SQLAlchemy
* Database migrations
* User relationships
* Pagination
* Search
* Internationalization
* JavaScript
* Notifications
* Background-job concepts
* APIs
* Docker and deployment concepts

Additional work on the project includes configuring and experimenting with supporting infrastructure such as MySQL, Elasticsearch, LibreTranslate, Docker Compose, persistent volumes, authenticated service communication, Railway deployment and OpenAPI documentation.

The tutorial series can be found here:

[The Flask Mega-Tutorial, Part I: Hello, World!](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

---

## Version

Current release:

```text
v1.0.0
```

This version represents the initial application release and its core Flask functionality.

---

## Author

**Rikesh Mandal**

Built as a practical Flask project while following Miguel Grinberg's Flask Mega-Tutorial and expanded through hands-on work with REST APIs, Docker-based infrastructure, databases, search, translation services, cloud deployment and API documentation.
