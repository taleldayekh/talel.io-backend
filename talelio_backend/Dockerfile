FROM python:3.9-alpine

ARG SRC_DIR=talelio_backend
ARG APP_DIR=app

WORKDIR /${APP_DIR}

ADD requirements.txt /${APP_DIR}/
ADD ${SRC_DIR}/ /${APP_DIR}/${SRC_DIR}/

# Pipenv is not used for dependencies here since the environment
# created by Pipenv won't be needed inside the Docker container.
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "-m", "talelio_backend.app"]
