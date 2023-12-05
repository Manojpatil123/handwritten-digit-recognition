# Handwritten Digit Recognition Web Service

This repository contains a Handwritten Digit Recognition service using a trained model on mnist dataset and a Flask-based web service, mysql database configure, deployment option of docker and Kubernetes.

# Setup Instructions

Prerequisites
Python 3.9
Docker
Kubernetes (kubectl)
Minikube (optional for local Kubernetes testing)

# Installation Steps

Clone this repository:

```bash
git clone https://github.com/Manojpatil123/handwritten-digit-recognition.git
cd handwritten-digit-recognition
```
Set up the Python environment:

``` bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
.\venv\Scripts\activate   # For Windows
pip install -r Requirements.txt

```
Download the pre-trained model (best_model.h5) and place it in the project directory.

Update the configuration file (config.json) with your database credentials and secret key.

# Running the Web Service Locally

Start the Flask server:

```bash
python app.py
```

Access the service at http://localhost:80 in your browser or via API requests.

# Building and Deploying with Docker and Kubernetes

# Deployment Instructions


1. Build the Docker image for your Flask application.
2. Push the Docker image to a container registry.
3. Deploy the application to Kubernetes using the Deployment YAML (`deployment.yaml`).
4. Apply the Service YAML (`service.yaml`) to expose the application.

### Example Commands:

```bash
docker build -t your-docker-image .
docker push your-docker-image:latest
kubectl apply -f deployment.yaml
```
To enable external access to your application, use an Ingress resource in Kubernetes.

Update the ingress.yaml file with your actual domain/host and service name.
Apply the Ingress configuration to Kubernetes.

```bash
kubectl apply -f ingress.yaml
```
Replace placeholders like <YOUR_HOST>, <YOUR_SERVICE_NAME>, and <YOUR_PORT> with the appropriate values in the YAML files 

# API Endpoints

/classify (POST): Accepts an image in base64 format and returns the predicted digit.
Example request body:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"image": "base64_encoded_image_data"}' http://localhost:5000/classify
```

/classify_file (POST): Accepts an uploaded image file and returns the predicted digit.
Example request body:

```bash
curl -X POST -F "file=@/path/to/your/image.jpg" http://localhost:5000/classify_file
```

# Notes

Ensure the database is properly configured before deploying the service.
