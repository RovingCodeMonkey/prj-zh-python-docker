# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# base
# this target stage defines a base environment in which shared
# dependencies are installed
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FROM python:3.9-slim-buster as base


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/code-challenge/.local/bin:${PATH}"
ENV PYTHONPATH=/usr/code-challenge/src
ENV PORT=5000
ENV HOST 0.0.0.0

EXPOSE 5000

RUN apt-get update \
  && apt-get install -y libpq-dev g++ curl \
  && groupadd code-challenge \
  && useradd -b /home -m -g code-challenge code-challenge

COPY --chown=code-challenge:code-challenge ./poetry.lock /usr/code-challenge/poetry.lock
COPY --chown=code-challenge:code-challenge ./pyproject.toml /usr/code-challenge/pyproject.toml

WORKDIR /usr/code-challenge

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry
RUN mkdir /home/pypoetry && chown -R code-challenge:code-challenge /home/pypoetry

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# development
# this target stage defines a development environment
# This includes an entire Postgres database for local testing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FROM base as development

RUN apt-get update \
  && apt-get install -y curl make nano libxml-xpath-perl

RUN apt-get install -y postgresql-client postgresql \
  && mkdir /var/lib/postgresql/pg-data \
  && chown -R code-challenge:code-challenge /var/lib/postgresql

COPY --chown=code-challenge:code-challenge . /usr/code-challenge

RUN poetry install

ENTRYPOINT ["/usr/code-challenge/build/entrypoint.dev.sh"]
