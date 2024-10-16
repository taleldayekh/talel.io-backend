FROM python:3.9-alpine

ARG SRC_DIR=talelio_backend
ARG APP_DIR=app
ARG SCRIPTS_DIR=scripts

# ARGs gets passed with the build command in the CD pipeline and sets all of the
# ENV variables in the container which are expected for running the application.
ARG ENV
ARG SECRET_KEY
ARG WHITELISTED_EMAILS
ARG EMAIL_USER
ARG EMAIL_PASS
ARG EMAIL_SERVER
ARG EMAIL_SENDER
ARG S3_BUCKET
ARG DB_URI
ARG HOST

ARG DB_HOST
ARG DB_PORT
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ENV ENV=${ENV}
ENV SECRET_KEY=${SECRET_KEY}
ENV WHITELISTED_EMAILS=${WHITELISTED_EMAILS}
ENV EMAIL_USER=${EMAIL_USER}
ENV EMAIL_PASS=${EMAIL_PASS}
ENV EMAIL_SERVER=${EMAIL_SERVER}
ENV EMAIL_SENDER=${EMAIL_SENDER}
ENV S3_BUCKET=${S3_BUCKET}
ENV DB_URI=${DB_URI}
ENV HOST=${HOST}

ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

WORKDIR /${APP_DIR}

ADD requirements.txt /${APP_DIR}/
ADD ${SRC_DIR}/ /${APP_DIR}/${SRC_DIR}/
ADD ${SCRIPTS_DIR}/backup_postgres_db.sh /${APP_DIR}/

# Dependencies necessary for pip installing psycopg2 and pillow on the Python alpine image
# are added before installing the ones from the requirements.txt file. They are added in a
# virtual environment and later removed to reduce the image size.
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-dependencies \
    postgresql-dev \
    gcc \
    musl-dev \
    zlib-dev \
    jpeg-dev \
    && python3 -m pip install --no-cache-dir -r requirements.txt \
    && apk --no-cache del .build-dependencies

RUN chmod u+x ./${SRC_DIR}/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./talelio_backend/entrypoint.sh"]
