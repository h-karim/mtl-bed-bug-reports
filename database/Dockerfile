FROM postgres
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV PYTHONPATH "${PYTHONPATH}:/"

WORKDIR /src
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./src/pyproject.toml ./src/poetry.lock* ./
RUN poetry install --no-root

COPY ./src .
