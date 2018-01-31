docker build -t carme/twitter:latest -t carme/twitter:v0.1 .
docker-compose -f docker-compose-CeleryExecutor.yml up -d
