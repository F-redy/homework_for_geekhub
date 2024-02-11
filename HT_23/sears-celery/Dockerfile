FROM python:3.12-slim

ENV PYTHONDONTWRTIRBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /code

COPY requirements requirements
RUN pip install --upgrade pip && \
    pip install -r requirements/development.txt --no-cache-dir


COPY . .

EXPOSE 8000