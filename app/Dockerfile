FROM python:3.11

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app

COPY ./src .

RUN useradd -d /app -r -U admin && chown admin:admin -R /app

USER admin