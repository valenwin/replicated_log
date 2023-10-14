# replicated_log app v1.0.0

## Start application locally

- **Build Docker image**

  ```bash
  docker build -t replicated-log-app .

- **Run Docker container**

  ```bash
  docker run -p 5001:5001 -p 5002:5002 -p 5003:5003 replicated-log-app

## Usage

### Master Service (Port 5001)

- **GET Request**

  Retrieve messages from the Master Service:

  ```bash
  curl --location 'http://localhost:5001/master/messages'
  
- **POST Request**

  ```bash
  curl --location 'http://localhost:5001/master/append' \
       --header 'Content-Type: application/json' \
       --data '{"message": "Hello."}'

### Secondary1 Service (Port 5002)

- **GET Request**

  Retrieve messages from the Secondary1 Service:

  ```bash
  curl --location 'http://localhost:5002/secondary1/messages'

### Secondary2 Service (Port 5003)

- **GET Request**

  Retrieve messages from the Secondary2 Service:

  ```bash
  curl --location 'http://localhost:5003/secondary2/messages'