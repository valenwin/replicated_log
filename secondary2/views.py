import asyncio
import logging

from flask import (
    Blueprint,
    request,
    jsonify,
)

secondary2 = Blueprint("secondary2", __name__)

logging.basicConfig(
    level=logging.DEBUG,  # Set the desired log level
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app_secondary2.log"),
        logging.StreamHandler(),
    ],
)

# Set up a set to keep track of acknowledged messages
acknowledged_messages = []


@secondary2.route("/")
def index():
    return "This is the main page for Secondary Server"


@secondary2.route("/replicate", methods=["POST"])
async def replicate_message():
    message = request.get_json()

    if "message" not in message:
        return jsonify({"error": "Message not provided"}), 400

    # Assuming that successful replication involves storing the message locally
    stored_message = message["id"]

    # Check if the message is already acknowledged
    if stored_message in acknowledged_messages:
        logging.info(f"Message is already added to Secondary 2: {message}")
        return jsonify({"acknowledged": True}), 200
    else:
        await asyncio.sleep(1)
        logging.info(f"Add message to Secondary 2: {message}")
        acknowledged_messages.append(message)

    return jsonify({"acknowledged": True}), 200


@secondary2.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(acknowledged_messages)
