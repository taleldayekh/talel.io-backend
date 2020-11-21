FROM python:3.9-alpine

ARG FLASK_APP_PATH=/server/talel_io/playground/app.py

ENV FLASK_APP=${FLASK_APP_PATH}

WORKDIR /server

COPY . /server

# Pipenv is not used to install dependencies since the environment
# created by Pipenv won't be needed inside the Docker container.
RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run --host=0.0.0.0

