# kjlcjp-erp-backend
Kawauchi Japanese Language Center is a global Brand for Japanese Language Training Canter. This repo is created for backend ERP solution. Main tech stack is Python, FastAPI, PostgreSQL,.

# For Dev Environment Docker build

## For development
docker-compose -f docker-compose.dev.yml --env-file .env.development up -d --build

## For production
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d --build

