import threading


class WriteConcernManager:
    def __init__(self):
        self.messages_conditions = {}
        self.lock = threading.Lock()

    def wait_for_write_concern(self, message_id, required_acks):
        with self.lock:
            condition = self.messages_conditions.setdefault(
                message_id, threading.Condition(self.lock)
            )
            condition.required_acks = required_acks
            condition.acks_received = 0

        with condition:
            while condition.acks_received < condition.required_acks:
                condition.wait()

    def acknowledge_message(self, message_id):
        with self.lock:
            condition = self.messages_conditions.get(message_id)

        if condition:
            with condition:
                condition.acks_received += 1
                if condition.acks_received >= condition.required_acks:
                    condition.notify_all()
