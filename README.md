# WealthWise Financials

## Prerequisites
- Docker Desktop

## Setup Instructions

1. **Install Docker Desktop:**  
   Download and install Docker Desktop from [here](https://www.docker.com/products/docker-desktop).  
   Note: It may prompt you to install and allow WSL (Windows Subsystem for Linux). If you have never had WSL on your machine, this will prompt a restart.

2. **Open the Repository:**

3. **Build and Run the Docker Container:**

   ```sh
   docker-compose up -d
   ```

## Starting the Container

1. **Start the Docker Container:**

   ```sh
   docker-compose up -d
   ```

2. **Open the Application:**  
   Open a web browser and go to: [http://localhost:8501](http://localhost:8501)

## Making Changes

1. **Make the Appropriate Changes to the Code.**

2. **Rebuild the Docker Image:**

   ```sh
   docker-compose build
   docker-compose down
   docker-compose up -d
   ```