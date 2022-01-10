FROM python:3.9.9-slim as python-base
# python
ENV PYTHONUNBUFFERED=1
# poetry
# https://python-poetry.org/docs/configuration/#using-environment-variables
ENV POETRY_VERSION=1.1.2
# make poetry install to this location
ENV POETRY_HOME="/opt/poetry"
# make poetry create the virtual environment in the project's root. It gets named `.venv`
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# do not ask any interactive question
ENV POETRY_NO_INTERACTION=1
# paths
# this is where our requirements + virtual environment will live
ENV PYSETUP_PATH="/opt/pysetup"
ENV VENV_PATH="/opt/pysetup/.venv"
# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN apt-get update && apt-get install --no-install-recommends -y curl
# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

# `production` image used for runtime
FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY rentabot /app/rentabot
WORKDIR /app/rentabot

ENV PYTHONPATH=/app/rentabot
CMD ["scrapy", "crawl", "snimaem-sami"]
