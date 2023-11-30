import logging
from flask import Blueprint, request, jsonify
from utils import SecondaryServer

secondary2 = Blueprint("secondary2", __name__)
secondary_server = SecondaryServer()

logging.basicConfig(
    level=logging.DEBUG,  # Set the desired log level
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app_secondary2.log"),
        logging.StreamHandler(),
    ],
)


@secondary2.route("/")
def index():
    return "This is the main page for Secondary 2 Server"


@secondary2.route("/replicate", methods=["POST"])
def replicate_message():
    message = request.get_json()

    if "sequence_number" not in message or "id" not in message:
        return jsonify({"error": "Missing sequence number or message ID"}), 400

    # Process the message using the SecondaryServer instance
    result = secondary_server.process_message(message)

    if result == "Message processed":
        logging.info(f"Message {message['id']} processed by Secondary 2.")
        return jsonify({"acknowledged": True}), 200
    elif result == "Message already processed":
        # The message was already processed, acknowledge to prevent resending.
        logging.info(f"Message {message['id']} already processed by Secondary 2.")
        return jsonify({"acknowledged": True}), 200
    else:
        # An error occurred while processing the message.
        logging.error(f"Failed to process message {message['id']} by Secondary 2: {result}")
        return jsonify({"error": result}), 500


@secondary2.route("/messages", methods=["GET"])
def get_messages():
    # Return the ordered list of messages
    messages = secondary_server.get_ordered_messages()
    return jsonify(messages)
