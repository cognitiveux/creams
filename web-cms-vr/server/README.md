# CREAMS Project
CREAMS backend API

# Local development

# Create docker network if it doesn't exist
docker network create web

# Build the docker image
cd creams/server/

docker-compose build --no-cache # if you want to rebuild everything from scratch

or:

docker-compose build

# Start the containers
cd creams/server/

docker-compose up

# Load additional data

run the vr_templates.sql in the postgres container in order to load the templates for VR exhibitions

# Stop the containers
Either stop them through the Docker Desktop app, or run in another terminal the following commands:

cd creams/server/

docker-compose stop

# Links
- Documentation: http://localhost:10000/web_app/doc/
- Interactive Demo: http://localhost:10000/web_app/demo/
- Index: http://localhost:10000/web_app/index.html