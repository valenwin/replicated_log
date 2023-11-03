from flask import (
    Blueprint,
    request,
    jsonify,
)

from utils import (
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
        "message": "Hello!",
        "write_concern": 2
    }
    """
    req_data = request.get_json()
    message_content = req_data.get("message")
    write_concern = req_data.get("write_concern", 1)  # Default write concern is 1

    if not message_content:
        return jsonify({"error": "Message not provided"}), 400

    # Generate a unique message ID for deduplication and ordering
    message_id = generate_unique_message_id()

    # Avoid duplication by checking if the message ID already exists
    existing_message = next((m for m in in_memory_list if m["id"] == message_id), None)
    if existing_message:
        # If it exists, you might want to update it, ignore it, or throw an error, based on your use case
        return jsonify({"error": "Duplicate message"}), 409

    message_with_id = {"id": message_id, "message": message_content}
    in_memory_list.append(message_with_id)

    # Asynchronously replicate the message to the secondary servers
    replication_result = await replicate_to_secondaries(
        message_with_id, message_id, write_concern
    )

    if "Write concern not met" in replication_result:
        # Accepted but not completed replication
        return (
            jsonify({"warning": replication_result}),
            202,
        )
    else:
        # Created with successful replication
        return (
            jsonify({"status": replication_result}),
            201,
        )


@master.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(in_memory_list)
