# Stop and remove any existing containers
docker-compose -f ../docker/docker-compose.yml down

# Build the Docker image
docker-compose -f ../docker/docker-compose.yml build

# Start the Docker containers
docker-compose -f ../docker/docker-compose.yml up -d