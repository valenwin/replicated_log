import uuid
import time

import requests
import logging

from decouple import config

# List of URLs for all Secondary servers
secondary_urls = config("SECONDARY_URLS").split(",")

logging.basicConfig(
    level=logging.DEBUG,  # Set the desired log level
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app_master.log"),  # Log to a file
        logging.StreamHandler(),  # Log to the console
    ],
)


def generate_unique_message_id():
    unique_part = str(uuid.uuid4())
    timestamp_part = str(int(time.time()))
    message_id = f"{unique_part}-{timestamp_part}"
    return message_id


def replicate_to_secondaries(message: dict, message_id: str):
    # Initialize a list to store ACK statuses from Secondaries
    ack_statuses = []
    acknowledgments = {}

    message["id"] = message_id

    # Iterate over all Secondary URLs
    for secondary_url in secondary_urls:
        try:
            # Send the message to the Secondary
            response = requests.post(f"{secondary_url}/replicate", json=message)

            acknowledgments[secondary_url] = message

            # Check if the Secondary acknowledged the message
            # the acknowledgment logic in Secondary services
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
