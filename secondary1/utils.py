class ReplicationLog:
    def __init__(self):
        self.messages = {}  # Store messages using sequence number as key
        self.processed_ids = set()  # Keep track of processed message IDs for deduplication
        self.last_sequence_number = 0  # Keep track of the last sequence number

    def acknowledge_message(self, sequence_number, message_id, message):
        if sequence_number <= self.last_sequence_number:
            # Handle the ordering issue - we've already processed this sequence number
            return False, "Ordering issue detected - message is out of sequence"

        if message_id in self.processed_ids:
            # Message already acknowledged
            return True, "Message already acknowledged"

        # If there's a gap, we're missing a message, so don't acknowledge this one yet
        if sequence_number != self.last_sequence_number + 1:
            return False, "Message out of order - waiting for earlier messages"

        # Acknowledge and store the message
        self.messages[sequence_number] = message
        self.processed_ids.add(message_id)
        self.last_sequence_number = sequence_number  # Update the last processed sequence number

        return True, "Message acknowledged"

    def get_ordered_messages(self):
        # Returns a list of all messages in order
        ordered_messages = [self.messages[seq] for seq in sorted(self.messages)]
        return ordered_messages


class SecondaryServer:
    def __init__(self):
        self.message_log = []
        self.processed_ids = set()
        self.expected_sequence_number = 1
        self.out_of_order_messages = {}

    def process_message(self, message):
        message_id = message['id']
        sequence_number = message['sequence_number']

        # Deduplication check
        if message_id in self.processed_ids:
            return "Message already processed"

        # Total order processing
        if sequence_number == self.expected_sequence_number:
            self.append_to_log(message)
            self.expected_sequence_number += 1

            # Check if next messages are waiting in the buffer
            while self.expected_sequence_number in self.out_of_order_messages:
                self.append_to_log(self.out_of_order_messages.pop(self.expected_sequence_number))
                self.expected_sequence_number += 1
        else:
            # Store out-of-order messages in a buffer
            self.out_of_order_messages[sequence_number] = message

        return "Message processed"

    def append_to_log(self, message):
        # Append the message to the log and mark it as processed
        self.message_log.append(message)
        self.processed_ids.add(message['id'])

    def get_ordered_messages(self):
        # Returns all messages in the order of their sequence numbers
        return [self.message_log[seq] for seq in sorted(self.message_log)]
