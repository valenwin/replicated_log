import logging

from flask import (
    Blueprint,
    request,
    jsonify,
)

# Create a Blueprint instance
secondary1 = Blueprint('secondary1', __name__)

logging.basicConfig(
    level=logging.DEBUG,  # Set the desired log level
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('app_secondary.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)


# Define routes and views within the Blueprint
@secondary1.route('/')
def index():
    return 'This is the main page'


# @secondary1.route('/replicate', methods=['POST'])
# def replicate_message():
#     message = request.get_json()
#
#     # Implement your acknowledgment logic here
#     # For example, you can assume successful replication for this example
#     return jsonify({"acknowledged": True})

# Set up a set to keep track of acknowledged messages
acknowledged_messages = []


@secondary1.route('/replicate', methods=['POST'])
def replicate_message():
    message = request.get_json()
    print(message)
    #
    if 'message' not in message:
        return jsonify({"error": "Message not provided"}), 400

    # Assuming that successful replication involves storing the message locally
    stored_message = message['message']

    # Check if the message is already acknowledged
    # if stored_message in acknowledged_messages:
    #     return jsonify({"acknowledged": True}), 200

    # Implement your acknowledgment logic here
    # For example, you can log the received message and mark it as acknowledged
    acknowledged_messages.append(message)

    return jsonify({"acknowledged": True}), 200


@secondary1.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(acknowledged_messages)
