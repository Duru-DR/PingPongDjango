FROM python:3.11.9-bookworm

RUN apt-get update

ENV PYTHONDONTWRITEBYTECODE TRUE
ENV PYTHONUNBUFFERED TRUE

WORKDIR /server

RUN pip install --upgrade pip
COPY requirements.txt /server/
RUN pip install -r requirements.txt

COPY . /server/

CMD [ "bash", "-c", "python3 manage.py makemigrations authentication && python3 manage.py makemigrations && python3 manage.py migrate && daphne -b 0.0.0.0 -p 8800 config.asgi:application" ]
