import time

import requests
from flask import Blueprint, request, jsonify
from decouple import config
from master.manager import WriteConcernManager
from apscheduler.schedulers.background import BackgroundScheduler
from utils import (
    replicate_to_secondaries,
    generate_unique_message_id,
)

master = Blueprint("master", __name__)
write_concern_manager = WriteConcernManager()

secondary_urls = config("SECONDARY_URLS").split(",")
secondary_statuses = {url: "Unknown" for url in secondary_urls}

# In-memory list to store messages
in_memory_list = []


def send_heartbeat(secondary_url):
    try:
        response = requests.get(f"{secondary_url}/health")
        secondary_statuses[secondary_url] = "Healthy" if response.status_code == 200 else "Suspected"
    except requests.exceptions.RequestException:
        secondary_statuses[secondary_url] = "Unhealthy"


def check_quorum():
    healthy_count = sum(status == "Healthy" for status in secondary_statuses.values())
    return healthy_count >= len(secondary_urls) // 2 + 1


scheduler = BackgroundScheduler()
scheduler.add_job(
    lambda: [send_heartbeat(url) for url in secondary_urls], 'interval', seconds=5
)
scheduler.start()


@master.route("/")
def index():
    return "This is the main page for the Master Server"


@master.route("/append", methods=["POST"])
def append_message():
    if not check_quorum():
        return jsonify({"error": "No quorum, master is in read-only mode."}), 503

    req_data = request.get_json()
    message_content = req_data.get("message")
    write_concern = req_data.get("write_concern", 1)

    if not message_content:
        return jsonify({"error": "Message content is required."}), 400

    message_id = generate_unique_message_id()

    # Check for duplicate message IDs
    if any(msg['id'] == message_id for msg in in_memory_list):
        return jsonify({"error": "Duplicate message ID."}), 409

    # Create the message with a unique ID
    message_with_id = {
        "id": message_id,
        "message": message_content,
        "timestamp": int(time.time()),
    }
    in_memory_list.append(message_with_id)

    # Replicate the message to secondary servers
    # Note: Modify replicate_to_secondaries to handle the write concern and replication result.
    replicate_to_secondaries(message_with_id, message_id, write_concern)

    # Wait for the write concern to be satisfied
    try:
        write_concern_manager.wait_for_write_concern(message_id, write_concern)
    except TimeoutError:  # You should define a timeout mechanism in WriteConcernManager
        return jsonify({"error": "Write concern not met within the expected time."}), 408

    return jsonify({"status": "Message appended with required write concern"}), 201


@master.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(in_memory_list)


@master.route('/health', methods=['GET'])
def health_check():
    # Return the master's view of the health of the system
    return jsonify(secondary_statuses)
