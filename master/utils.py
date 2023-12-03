import random
import uuid
import time
import asyncio
import requests
import logging

from decouple import config
from requests.exceptions import RequestException
from requests.exceptions import ConnectionError, HTTPError, Timeout, TooManyRedirects

# Configuration for retries
MAX_RETRIES = 5
BASE_DELAY = 0.1  # seconds

# List of URLs for all Secondary servers
# example from .env file
# http://secondary1:5002/secondary1,http://secondary2:5003/secondary2
secondary_urls = config("SECONDARY_URLS").split(",")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app_master.log"),
        logging.StreamHandler(),
    ],
)


def generate_unique_message_id():
    unique_part = str(uuid.uuid4())
    timestamp_part = str(int(time.time()))
    message_id = f"{unique_part}-{timestamp_part}"
    return message_id


async def replicate_to_secondaries(message: dict, message_id: str, write_concern: int):
    # Store ACKs received from Secondaries
    acks_received = 0

    message["id"] = message_id

    # Set up tasks for all secondaries
    secondary_tasks = []
    for secondary_url in secondary_urls:
        task = asyncio.create_task(replicate_to_secondary(secondary_url, message))
        secondary_tasks.append(task)

    # Await the replication tasks and check for acknowledgements
    for future in asyncio.as_completed(secondary_tasks):
        secondary_ack, _ = await future
        if secondary_ack:
            acks_received += 1
            # If we've met the write concern, we can respond successfully
            if acks_received >= write_concern:
                break

    # Check if write concern level is met
    if acks_received >= write_concern:
        logging.info(
            f"Message {message_id} replicated to {acks_received} secondaries, meeting write concern of {write_concern}."
        )
        return "Message replicated according to write concern."
    else:
        logging.warning(
            f"Message {message_id} did not meet write concern. Only {acks_received} secondaries acknowledged."
        )
        return "Write concern not met; message may not be fully replicated."


async def replicate_to_secondary(secondary_url: str, message: dict):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            logging.debug(
                f"Sending message {message['id']} to {secondary_url}. Attempt: {retries + 1}"
            )
            response = await asyncio.to_thread(
                requests.post, f"{secondary_url}/replicate", json=message
            )
            response.raise_for_status()
            logging.debug(
                f"Successfully sent message {message['id']} to {secondary_url}"
            )
            return True, secondary_url
        except RequestException as e:
            logging.warning(
                f"Failed to send message {message['id']} to {secondary_url}: {e}"
            )
            if retries >= MAX_RETRIES - 1:
                logging.error(
                    f"Max retries exceeded for message {message['id']} to {secondary_url}"
                )
                break
            delay = BASE_DELAY * (2**retries) + random.uniform(0, 1)
            logging.info(f"Retrying in {delay:.2f} seconds...")
            await asyncio.sleep(delay)
            retries += 1

    return False, secondary_url
