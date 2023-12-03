from flask import Blueprint, request, jsonify, make_response
import asyncio
import logging
from utils import SecondaryServer

secondary1 = Blueprint("secondary1", __name__)
secondary_server = SecondaryServer()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app_secondary1.log"),
        logging.StreamHandler(),
    ],
)


@secondary1.route("/")
def index():
    return "This is the main page for Secondary 1 Server"


@secondary1.route("/replicate", methods=["POST"])
async def replicate_message():
    await asyncio.sleep(1)

    message = request.get_json()
    if "sequence_number" not in message or "id" not in message:
        return jsonify({"error": "Missing sequence number or message ID"}), 400

    result = secondary_server.process_message(message)

    if result == "Message processed":
        logging.info(f"Message {message['id']} processed by Secondary 1.")
        return jsonify({"acknowledged": True}), 200
    elif result == "Message already processed":
        logging.info(f"Message {message['id']} already processed by Secondary 1.")
        # Acknowledge to prevent resending
        return jsonify({"acknowledged": True}), 200
    else:
        logging.error(
            f"Failed to process message {message['id']} by Secondary 1: {result}"
        )
        return jsonify({"error": result}), 500


@secondary1.route("/messages", methods=["GET"])
def get_messages():
    # Return the ordered list of messages
    messages = secondary_server.get_ordered_messages()
    return jsonify(messages)


@secondary1.route("/health", methods=["GET"])
def health_check():
    response = make_response("", 200)
    return response
