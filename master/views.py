from flask import (
    Blueprint,
    request,
    jsonify,
)

from master.utils import replicate_to_secondaries

# Create a Blueprint instance
master = Blueprint('master', __name__)

# In-memory list to store messages
in_memory_list = []


# Define routes and views within the Blueprint
@master.route('/')
def index():
    return 'This is the main page'


@master.route('/append', methods=['POST'])
def append_message():
    """
    {
        "message": "Hello!"
    }
    """
    message = request.get_json()

    if 'message' not in message:
        return jsonify({"error": "Message not provided"}), 400

    in_memory_list.append(message)
    replication_result = replicate_to_secondaries(message)
    return replication_result


@master.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(in_memory_list)
