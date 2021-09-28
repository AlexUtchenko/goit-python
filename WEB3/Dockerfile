FROM python:3.9-slim-buster

WORKDIR app

RUN pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system --deploy

COPY test_gotovo test_gotovo

RUN pip install ./test_gotovo

CMD python cli_com

