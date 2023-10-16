from flask import (
    Blueprint,
    request,
    jsonify,
)

from utils import (
    replicate_to_secondaries_async,
    replicate_to_secondaries,
    generate_unique_message_id,
)

master = Blueprint("master", __name__)

# In-memory list to store messages
in_memory_list = []


@master.route("/")
def index():
    return "This is the main page for Mater Server"


@master.route("/append", methods=["POST"])
async def append_message():
    """
    Request json body example:
    {
        "message": "Hello!"
    }
    """
    message = request.get_json()

    if "message" not in message:
        return jsonify({"error": "Message not provided"}), 400

    in_memory_list.append(message)

    message_id = generate_unique_message_id()
    replication_result = await replicate_to_secondaries(message, message_id)
    return replication_result


@master.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(in_memory_list)
