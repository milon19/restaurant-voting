# Restaurant Voting System

## Installation

#### Installation using Docker

- Set up `.env` file with proper configuration. The required fields in the `.env.example`.

> See `.env.example` for better understanding with sample value

```dotenv
DEBUG=True  # This is optional, Default: False
DJANGO_SECRET=''  # Value given in .env.example

COMPOSE_FILE=docker-compose.yml
COMPOSE_PROJECT_NAME=restaurant-voting
WEB_APP_PORT=8000
POSTGRES_PASSWORD=<Your Postgres Password>
POSTGRES_PORT=<Postgres Port> # usually: 5432
POSTGRES_HOST=<Postgres Host> # If you run it with docker then value will be 'postgres'. Otherwise 'localhost'
DOCKER_POSTGRES_PORT=<Port> # different from local machine postgres port, like: 5455
POSTGRES_DB=<Database Name>
POSTGRES_USER=<Database User>
JWT_SECRET=<JWT secret>
```

- You are all set as your .env file is set too. Now run
- ```shell
   docker-compose up -d --build
  ```
- Your project should be running soon.

#### Manual installation.

- Go to project root where `manage.py` file is located.
- Create a virtual environment.

```shell
virtualenv <name>
```

- Active the environment.

```shell
source ./<name>/bin/activate
```

- Install `requirements.txt`

```shell
pip install -r requirements.txt
```

- Setup the `.env` with the above configuration.
- Now open a terminal and run the migration command to migrate db. (You need to create a db first.)
- ```shell
  python manage.py migrate
  ```
- Now, run the project with a flowing command.
- ```shell
   python manage.py runserver
  ```

Your project should be running.

### A database will be automatically created when you run with Docker. If you want to run manually you need to create a database with `<POSTGRES_DB>` name.

> NOTE: This installation is only used for development.

## Note about project

- All date times in the project are in UTC.
- To run the test:

```shell
python manage.py test
```
