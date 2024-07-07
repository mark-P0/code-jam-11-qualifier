## Base image
FROM nikolaik/python-nodejs:python3.12-nodejs22-slim

# TODO Use different Dockerfiles? Multi-stage?
RUN npm i -g nodemon

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
