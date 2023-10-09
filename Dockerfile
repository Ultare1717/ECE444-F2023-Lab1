# syntax=docker/dockerfile:1

FROM python:3.9.6
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get -y install gcc
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=hello.py
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]