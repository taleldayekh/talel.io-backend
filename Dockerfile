FROM python:3.9-alpine

ARG SRC_DIR=talel_io

ENV FLASK_APP=playground/app.py

WORKDIR /${SRC_DIR}

COPY requirements.txt ${SRC_DIR} /${SRC_DIR}/

# Pipenv is not used for dependencies here since the environment
# created by Pipenv won't be needed inside the Docker container.
RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run --host=0.0.0.0

