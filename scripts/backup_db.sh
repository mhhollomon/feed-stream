#!/usr/bin/env bash
set -e
#set -x

DEST_DIR=$1
SOURCE_DB=$2


if [ -z "${DEST_DIR}" ]; then
    echo "No destination directory specified"
    exit 3
fi

if [ -z "$SOURCE_DB" ]; then
    path=${0%/*}
    env_path="${path}/../.env"

    if [ -f $env_path ]; then
        . ${env_path}
        SOURCE_DB=${DATABASE_LOCATION}
    fi

    if [ -z "$SOURCE_DB" ]; then
        echo "No Source Database given"
        exit 3
    fi
fi

BASE_DB_NAME=${SOURCE_DB##*/}
EXTEN=${BASE_DB_NAME##*.}
BASE_DB_NAME=${BASE_DB_NAME%.*}


DATE=$(date -I)
DB_FILE="${BASE_DB_NAME}-${DATE}.${EXTEN}"

echo "Backing up to ${SOURCE_DB} to ${DB_FILE}"

sqlite3 $SOURCE_DB ".backup $DEST_DIR/$DB_FILE"