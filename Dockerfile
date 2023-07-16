FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ARG APP_DIR=/app

# install app
ENV POETRY_HOME="/.poetry"

RUN apt-get -y -q update && \
    apt-get -y -q install curl libffi-dev && \
    curl -sSL https://install.python-poetry.org | python - --version 1.3.2 && \
    ${POETRY_HOME}/venv/bin/pip install keyrings.google-artifactregistry-auth && \
    apt-get autoremove -y curl && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="${POETRY_HOME}/bin:${PATH}"
RUN poetry config virtualenvs.in-project true
ENV PATH="${APP_DIR}/.venv/bin:${PATH}"

WORKDIR $APP_DIR

COPY pyproject.toml poetry.lock ./
RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
RUN poetry install --without dev,test --no-root --no-interaction

COPY src src

CMD poetry run python -m src.job