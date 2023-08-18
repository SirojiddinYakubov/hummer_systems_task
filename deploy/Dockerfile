FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y netcat-traditional vim
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /code

COPY pyproject.toml poetry.lock* /code/
#COPY deploy/requirements.txt requirements.txt

RUN poetry install --no-root
RUN echo "Successfully installed required packages"
RUN #pip install --upgrade pip && pip install -r requirements.txt

COPY . /code
COPY deploy/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]

