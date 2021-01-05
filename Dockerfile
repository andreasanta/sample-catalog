# Pull a base image
FROM python:3.9-alpine

# Set database host (on network)
ENV DB_HOST='springcat_db'

# Install Postgres compilation reqs
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Install requirements
WORKDIR /code
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

# Copy the project files into the working directory
COPY . /code/

# Expose default django port
EXPOSE 8000