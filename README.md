# Pycommerce

## Overview (Work in Progress)

<p align="left">
  <a href="https://skillicons.dev">
    <img src="https://skills.thijs.gg/icons?i=py,fastapi,postgres,docker&theme=dark" />
  </a>
</p>

`Pycommerce` is an example application built with modern Python following TDD, structured with a _variant_ of Clean Architecture, and using the technologies below:

- Language: [Python 3.11](https://www.python.org/)
- Container: [Docker](https://www.docker.com/)
- Package management: [Poetry](https://python-poetry.org/)
- Web framework: [FastAPI](https://fastapi.tiangolo.com/)
- Web server: [Uvicorn](http://www.uvicorn.org/)
- Database: [Postgres](https://www.postgresql.org/)
- Database migrations: [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- ORM: [SQLModel](https://sqlmodel.tiangolo.com/)
- Password hashing: [Passlib](https://passlib.readthedocs.io/)
- Authentication: [OAuth2 + JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- Data parsing and validation: [Pydantic](https://pydantic-docs.helpmanual.io/)
- Testing: [Pytest](https://docs.pytest.org/en/latest/)
- Linter: [Flake8](https://flake8.pycqa.org/en/latest/)
- Type checker: [Mypy](https://mypy.readthedocs.io/en/stable/index.html)
- Code formatter: [Black](https://github.com/psf/black)

## Usage

### Installing

Activate your Python [virtual environment](https://docs.python.org/3/library/venv.html) and run:

```sh
poetry install

# or

pip install .
```

### Configuration

`Pycommerce` uses environment variables for configuration. You can check all the available options [here](pycommerce/config.py). You can set them manually like this:

```sh
export DB_URL="<database_url>"
export JWT_SECRET_KEY="<my_super_secret_key>"
...
```

Or, you can create and fill a `.env` file using the [.env.example](.env.example) file as a reference.

### Tests

Run the automated tests with:

```sh
docker-compose up tests

# or, set the DB_URL env var to point to the testing database and run

pytest
```

### Running the Application

```sh
# Optionally, you can add pg-admin to the containers list

docker-compose up app pg-db -d

# or, set the DB_URL env var to point to the dev database, and run

alembic upgrade head && poetry run app

# or

alembic upgrade head && python -m pycommerce
```

Open the browser on [http://localhost:8080/docs](http://localhost:8080/docs) to see the OpenAPI docs:

![](docs/openapi.png)


⚠️ If you're not using Docker, remember to run the [init.sql](scripts/pg/init.sql) script to create the databases before running the application.

### Type Checking

```sh
mypy pycommerce tests
```

### Linting

```sh
flake8 pycommerce tests
```

### Code Formatting

```sh
black --check pycommerce tests
```

## Development Workflow

In order to enhance your development workflow and streamline the process of creating new features using TDD in Python, you can leverage [pytest-watch](https://pypi.org/project/pytest-watch/) (which is already included in the dependencies), to automatically trigger tests whenever a piece of code is modified. This helps to accelerate the feedback loop, allowing you to iterate more quickly and efficiently. For instance:

![](docs/tdd_workflow.gif)

## Project Structure

🚧 TBD

## Code Design

🚧 TBD

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
