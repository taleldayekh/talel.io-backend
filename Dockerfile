FROM python:3.9-alpine

ARG SRC_DIR=talel_io
ARG APP_DIR=app

WORKDIR /${APP_DIR}

ADD requirements.txt /${APP_DIR}/
ADD talel_io/ /${APP_DIR}/${SRC_DIR}/

# Pipenv is not used for dependencies here since the environment
# created by Pipenv won't be needed inside the Docker container.
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "talel_io.app"]
