# Pycommerce

## Overview (Work in Progress)

<p align="left">
  <a href="https://skillicons.dev">
    <img src="https://skills.thijs.gg/icons?i=py,fastapi,postgres,docker&theme=dark" />
  </a>
</p>

`Pycommerce` is an example application built with modern Python following TDD, structured with a _variant_  of Clean Architecture, and using the technologies below:

- Language: [Python 3.11](https://www.python.org/)
- Container: [Docker](https://www.docker.com/)
- Package management: [Poetry](https://python-poetry.org/)
- Web framework: [FastAPI](https://fastapi.tiangolo.com/)
- Web server: [Uvicorn](http://www.uvicorn.org/)
- Database: [Postgres](https://www.postgresql.org/)
- Database migrations: [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- ORM: [SQLModel](https://sqlmodel.tiangolo.com/)
- Password hashing: [Bcrypt](https://github.com/pyca/bcrypt/)
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

### Tests

Run the automated tests with:

```sh
docker-compose up tests

# or, set the DB_URL env var to point to the testing database (use the .env.example file as a reference), and run

pytest
```

### Running the Application

 ```sh
 # Optionally, you can add pg-admin to the containers list

 docker-compose up app pg-db -d

 # or, set the DB_URL env var to point to the dev database, and run
 
 poetry run app

 # or

 python -m pycommerce

 ```

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
