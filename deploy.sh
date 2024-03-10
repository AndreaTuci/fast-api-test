#!/bin/bash

if [ "$1" == "staging" ]; then
  ENV_FILE=".env.staging"
elif [ "$1" == "release" ]; then
  ENV_FILE=".env.production"
else
  ENV_FILE=".env.development"
fi

cp $ENV_FILE .env

echo "Deploying in $1 environment using $ENV_FILE..."

set -a
source .env
set +a

envsubst < docker-compose.template.yml > docker-compose.yml

docker-compose build
docker-compose up

echo "Deployment to $1 environment completed."
