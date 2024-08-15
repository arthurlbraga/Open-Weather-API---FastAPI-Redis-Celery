FROM python:3.12.5-slim-bookworm
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt