FROM python:3.11.2-alpine3.17 as base

FROM base as requirements

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /tmp

RUN apk --no-cache add \
    build-base \
    libffi-dev \
    musl \
    openssl-dev \
    gcc \
    libc-dev \
    linux-headers

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM base as final

WORKDIR /app

COPY --from=requirements /tmp/requirements.txt /code/requirements.txt

RUN apk --no-cache add \
    libffi-dev \
    gcc \
    libc-dev

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /app

CMD ["python", "-m" , "pycommerce"]
