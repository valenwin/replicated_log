# replicated_log app v2.0.0

## Start application on your local machine

- **Build Docker images**

  ```bash
  docker-compose build

- **Run Docker containers**

  ```bash
  docker-compose up -d

## Usage

### Master Service (Port 5001)

- **GET Request**

  Retrieve messages from the Master Service:

  ```bash
  curl --location 'http://localhost:5001/master/messages'
  
- **POST Request**

  ```bash
  curl --location 'http://127.0.0.1:5001/master/append' \
  --header 'Content-Type: application/json' \
  --data '{
    "message": "Hello.",
    "write_concern": 2
  }'

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