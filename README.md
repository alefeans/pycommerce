# Pycommerce

## Overview (Work in Progress)

<p align="left">
  <a href="https://skillicons.dev">
    <img src="https://skills.thijs.gg/icons?i=py,fastapi,postgres,docker&theme=dark" />
  </a>
</p>

`Pycommerce` is an example application built with modern Python using DDD, TDD, a "variant" of Clean Architecture, and the following technologies:


- Language: [Python 3.11](https://www.python.org/)
- Package management: [Poetry](https://python-poetry.org/)
- Web framework: [FastAPI](https://fastapi.tiangolo.com/)
- Production web server: [Uvicorn](http://www.uvicorn.org/)
- Relational database: [Postgres](https://www.postgresql.org/)
- Relational database migrations: [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- Relational ORM: [SQLModel](https://sqlmodel.tiangolo.com/)
- Functional programming utilities: [Toolz](https://toolz.readthedocs.io/en/latest/)
- Password hashing: [Bcrypt](https://github.com/pyca/bcrypt/)
- Data parsing and validation: [Pydantic](https://pydantic-docs.helpmanual.io/)
- Testing: [Pytest](https://docs.pytest.org/en/latest/)
- Linter: [Flake8](https://flake8.pycqa.org/en/latest/)
- Type checker: [Mypy](https://mypy.readthedocs.io/en/stable/index.html)
- Code formatter: [Black](https://github.com/psf/black)

## Usage

First, activate your virtual environment and run:

```sh
poetry install

# or

pip install .
```

Create a `.env` file, fill it with the required environment variables using the [.env.example](.env.example) file as an example, and run:

```sh
poetry run app

# or

python pycommerce
```

## Docker

🚧 TBD

## Tests

First, change the `DB_URL` env var to point to the test database, then run:

```sh
# add --cov to generate the code coverage report

poetry run pytest

# or

pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
