FROM python:3.9.8-slim as base

ARG PYSETUP_PATH
ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	\
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \
	\
	POETRY_VERSION=1.1.11 \
	POETRY_HOME="/opt/poetry" \
	POETRY_VIRTUALENVS_IN_PROJECT=true \
	PYSETUP_PATH="/opt/pysetup" \
	POETRY_NO_INTERACTION=1 \
	\
	VENV_PATH="/opt/pysetup/.venv" \
	\
	BANTER_BUS_CORE_API_WEB_HOST="0.0.0.0" \
	BANTER_BUS_CORE_API_WEB_PORT=8080

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM base as builder

RUN apt-get update && apt-get install curl -y
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev


FROM base as production

ENV BANTER_BUS_CORE_API_ENVIRONMENT=production
COPY --from=builder $VENV_PATH $VENV_PATH
COPY ./app /app

WORKDIR /
EXPOSE 8080
CMD uvicorn app:app --host ${BANTER_BUS_CORE_API_WEB_HOST} --port ${BANTER_BUS_CORE_API_WEB_PORT}


FROM base as development

ENV BANTER_BUS_CORE_API_ENVIRONMENT=development
WORKDIR $PYSETUP_PATH

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install

WORKDIR /
EXPOSE 8080
CMD uvicorn --reload app:app --host ${BANTER_BUS_CORE_API_WEB_HOST} --port ${BANTER_BUS_CORE_API_WEB_PORT}
