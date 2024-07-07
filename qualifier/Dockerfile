## Base image
FROM python:3.12.2-slim

## Working directory inside container
## Usually suggested by the providers of the base image
WORKDIR /usr/src/app

## Dependencies
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

## Copy source files
COPY . .

## Run application
CMD [ "python", "qualifier.py" ]
