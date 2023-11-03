import logging

from flask import (
    Blueprint,
    request,
    jsonify,
)

from replication_log import ReplicationLog

secondary2 = Blueprint("secondary2", __name__)
# Create an instance of the log
replication_log = ReplicationLog()

logging.basicConfig(
    level=logging.DEBUG,  # Set the desired log level
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app_secondary2.log"),
        logging.StreamHandler(),
    ],
)

# Use a dictionary to keep track of acknowledged messages with their timestamps
acknowledged_messages = {}


@secondary2.route("/")
def index():
    return "This is the main page for Secondary 2 Server"


@secondary2.route("/replicate", methods=["POST"])
async def replicate_message():
    message = request.get_json()

    if "message" not in message or "timestamp" not in message:
        return jsonify({"error": "Message or timestamp not provided"}), 400

    message_id = message["id"]
    message_timestamp = message["timestamp"]

    acknowledged, error = replication_log.acknowledge_message(
        message_id, message_timestamp, message
    )

    if not acknowledged:
        if error:
            logging.error(f"Error acknowledging message {message_id}: {error}")
            return jsonify({"error": error}), 500
        else:
            logging.info(f"Message {message_id} is already added to Secondary 2.")
            return jsonify({"acknowledged": True}), 200

    logging.info(f"Adding message {message_id} to Secondary 2.")
    return jsonify({"acknowledged": True}), 200


@secondary2.route("/messages", methods=["GET"])
def get_messages():
    messages = replication_log.get_messages()
    return jsonify(messages)
