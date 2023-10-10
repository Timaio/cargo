FROM python:3.8-slim

WORKDIR /cargo
COPY . .
RUN pip install -r requirements.txt
RUN adduser --disabled-password cargo-user
EXPOSE 8000
USER cargo-user

