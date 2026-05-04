#!/bin/bash

# This script deploys the Telehealth Hypertension Predictive Analytics System

# Set environment variables
export FRONTEND_DIR="./frontend"
export BACKEND_DIR="./backend"
export DOCKER_COMPOSE_FILE="./docker/docker-compose.yml"

# Build frontend
echo "Building frontend..."
cd $FRONTEND_DIR
npm install
npm run build

# Build backend
echo "Building backend..."
cd $BACKEND_DIR
pip install -r requirements.txt

# Deploy using Docker Compose
echo "Deploying application using Docker Compose..."
cd ..
docker-compose -f $DOCKER_COMPOSE_FILE up --build -d

# Check if the deployment was successful
if [ $? -eq 0 ]; then
    echo "Deployment successful! The application is running."
else
    echo "Deployment failed. Please check the logs for more details."
fi

# End of script