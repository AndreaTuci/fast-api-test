# Fast API Test

## Description

This is a project that uses FastAPI.

## Example environment file

.env.development
```env
APP_ENV=development

# Db
DB_NAME=dev_db
DB_USER=dev_user
DB_PASSWORD=dev_password
DB_HOST=db
DB_PORT=5432

# FastAPI
API_RELOAD=true

#Nginx
NGINX_CONF=./nginx/development.conf
```

## Run project

```bash
./deploy.sh
```