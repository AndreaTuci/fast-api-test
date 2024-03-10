#!/bin/bash
set -a
source .env
set +a

envsubst < docker-compose.template.yml > docker-compose.yml
