# Organizer API

Task organizer REST API built with Flask, Flask-RESTX (Swagger/OpenAPI docs), SQLAlchemy and PostgreSQL, following a layered Repository / Service / Routes architecture.

## Running with Docker (recommended)

Requirements: [Docker](https://www.docker.com/) and Docker Compose.

```bash
git clone <this-repo-url>
cd organizer
cp .env.example .env
docker compose up --build
```

The API will be available at `http://localhost:5000`, with interactive Swagger docs at `http://localhost:5000/swagger.html`.

PostgreSQL is exposed on the host at port `55432` (mapped to the container's `5432`) in case you want to connect with a database client. The API itself talks to the `db` service directly over the internal Docker network.

To stop everything:

```bash
docker compose down
```

## Running locally without Docker

Requirements: Python 3.12+, a running PostgreSQL instance.

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux / macOS

pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`) with `POSTGRES_HOST` pointing at your local Postgres instance (e.g. `localhost`) and the matching port/credentials.

```bash
python -m app.app
```

## Running tests

```bash
pytest
```

Unit tests exercise the service layer with mocked repositories; integration tests exercise the Flask API end-to-end and need a reachable PostgreSQL database (same `.env` configuration as above).

## Project structure

```
app/
  models/         SQLAlchemy ORM models (User, Task)
  repositories/    Data access layer
  services/        Business logic layer
  routes/          Flask-RESTX namespaces / HTTP layer
  database.py      Engine/session setup
  swagger.py       Flask-RESTX Api instance
  app.py           Application entrypoint
tests/
  unit/            Service layer tests with mocked repositories
  integration/      API tests against a real database
```

## API overview

- `POST /users/register` - register a new user
- `POST /users/login` - log in
- `PUT /users/change-password` - change password
- `POST /tasks` - create a task
- `GET /tasks/user/<user_id>` - list a user's tasks
- `GET /tasks/user/<user_id>/<date>` - list a user's tasks for a given date (`YYYY-MM-DD`)
- `PUT /tasks/<task_id>` - update a task
- `DELETE /tasks/<task_id>` - delete a task
