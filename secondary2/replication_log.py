class ReplicationLog:
    def __init__(self):
        self.acknowledged_messages = []
        self.last_acknowledged_time = 0

    def acknowledge_message(self, message_id, message_timestamp, message):
        if message_timestamp < self.last_acknowledged_time:
            # Handle the ordering issue
            return False, "Ordering issue detected"

        if any(
                msg["message"]["id"] == message_id for msg in self.acknowledged_messages
        ):
            # Message already acknowledged
            return True, None

        # Acknowledge the message
        self.acknowledged_messages.append(
            {"message": message, "timestamp": message_timestamp}
        )
        self.last_acknowledged_time = message_timestamp
        return True, None

    def get_messages(self):
        # Returns a list of all messages sorted by timestamp
        return sorted(
            self.acknowledged_messages,
            key=lambda x: x['timestamp']
        )
