#!/usr/bin/env sh

POSTGRES_CONTAINER_ID=$(docker ps -qf "name=.*postgres.*")

DATE_BIN=$(command -v date)
TIMESTAMP=`${DATE_BIN} +%y%m%d-%H%M%S`

DB_BACKUP_DIR="talelio-db-backup"
DB_BACKUP_NAME="${DB_BACKUP_DIR}-${TIMESTAMP}.sql"

AWS_BIN=/usr/local/aws-cli/v2/current/bin/aws

if ! [ -d "$HOME/${DB_BACKUP_DIR}" ]; then
  echo "Creating backup directory"
  mkdir -p $HOME/${DB_BACKUP_DIR}
fi

echo "Creating database backup"
docker exec -t ${POSTGRES_CONTAINER_ID} pg_dump -c -U ${POSTGRES_USER} ${POSTGRES_DB} > $HOME/${DB_BACKUP_DIR}/${DB_BACKUP_NAME}

if [ -f "$HOME/${DB_BACKUP_DIR}/${DB_BACKUP_NAME}" ]; then
  echo "Uploading database backup to S3"
  $AWS_BIN s3 cp $HOME/${DB_BACKUP_DIR}/${DB_BACKUP_NAME} ${S3_URI}
  $AWS_BIN s3api head-object --bucket ${S3_BUCKET} --key ${S3_BUCKET_BACKUP_DIR}/${DB_BACKUP_NAME} || backup_failed=true

  if [ $backup_failed ]; then
    echo "S3 upload failed"
  else
    echo "Removing database backup file from EC2"
    rm $HOME/${DB_BACKUP_DIR}/${DB_BACKUP_NAME}
  fi
fi
