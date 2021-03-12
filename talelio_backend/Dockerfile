FROM python:3.8-alpine

ARG SRC_DIR=talelio_backend
ARG APP_DIR=app

WORKDIR /${APP_DIR}

ADD requirements.txt /${APP_DIR}/
ADD .env /${APP_DIR}/
ADD ${SRC_DIR}/ /${APP_DIR}/${SRC_DIR}/

# Dependencies necessary for pip installing psycopg2 on the Python alpine image
# are added before installing the ones from the requirements.txt file. They are
# added in a virtual environment and later removed to reduce the image size.
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-dependencies \
    postgresql-dev \
    gcc \
    musl-dev \
    && python3 -m pip install --no-cache-dir -r requirements.txt \
    && apk --no-cache del .build-dependencies

RUN chmod u+x ./${SRC_DIR}/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./talelio_backend/entrypoint.sh"]
