#!/bin/bash

# Define variables
DOCKERFILE_DIR="./"  # Directory containing the Dockerfile
IMAGE_NAME="my_app_image"
TAR_NAME="my_app_image.tar"
COMPOSE_FILE="docker-compose.yml"  # Local path to your docker-compose.yml
REMOTE_USER="root"
REMOTE_IP="167.172.44.204"
REMOTE_DIR="/root"

# Step 1: Build Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME $DOCKERFILE_DIR

# Step 2: Create a Docker tar from the image
echo "Creating Docker tar from image..."
docker save -o $TAR_NAME $IMAGE_NAME

# Step 3: Transfer the Docker tar and docker-compose.yml to the remote Droplet
echo "Transferring Docker tar and docker-compose.yml to remote Droplet..."
scp $TAR_NAME ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_DIR}
scp $COMPOSE_FILE ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_DIR}

# Step 4 and 5: SSH into the Droplet, Load the Docker image, and Run docker-compose
echo "SSHing into Droplet to load Docker image and run docker-compose..."
ssh ${REMOTE_USER}@${REMOTE_IP} << EOF
  cd ${REMOTE_DIR}
  docker load -i ${TAR_NAME}
  docker-compose up -d
EOF

# End of script
echo "Deployment completed."

