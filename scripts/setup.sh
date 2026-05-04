#!/bin/bash

# Setup script for the Telehealth Hypertension Predictive Analytics System

# Update package list and install necessary packages
echo "Updating package list..."
sudo apt-get update

# Install Python and pip
echo "Installing Python and pip..."
sudo apt-get install -y python3 python3-pip

# Install Node.js and npm
echo "Installing Node.js and npm..."
sudo apt-get install -y nodejs npm

# Install Docker
echo "Installing Docker..."
sudo apt-get install -y docker.io

# Install Docker Compose
echo "Installing Docker Compose..."
sudo apt-get install -y docker-compose

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r backend/requirements.txt

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install

# Return to the root directory
cd ..

# Setup complete
echo "Setup complete! You can now run the application."