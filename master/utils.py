import requests
import logging

# List of URLs for all Secondary servers
secondary_urls = ["http://localhost:5002/secondary1", "http://localhost:5003/secondary2"]

logging.basicConfig(
    level=logging.DEBUG,  # Set the desired log level
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('app_master.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)


def replicate_to_secondaries(message: str):
    # Initialize a list to store ACK statuses from Secondaries
    ack_statuses = []

    # Iterate over all Secondary URLs
    for secondary_url in secondary_urls:
        try:
            # Send the message to the Secondary
            response = requests.post(f"{secondary_url}/replicate", json=message)

            # Check if the Secondary acknowledged the message (you can define the acknowledgment logic in your Secondary services)
            if response.status_code == 200 and response.json().get("acknowledged"):
                ack_statuses.append(True)
            else:
                ack_statuses.append(False)
        except requests.exceptions.RequestException:
            # Handle exceptions such as connection errors here
            ack_statuses.append(False)

    # Check if all Secondaries acknowledged the message
    if all(ack_statuses):
        logging.info("Message replicated on all Secondaries")
        return "Message replicated on all Secondaries"
    else:
        logging.info("Failed to replicate message on all Secondaries")
        return "Failed to replicate message on all Secondaries"
