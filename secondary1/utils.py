class SecondaryServer:
    def __init__(self):
        self.message_log = {}
        self.processed_ids = set()
        self.expected_sequence_number = 1
        self.out_of_order_messages = {}

    def process_message(self, message):
        message_id = message["id"]
        sequence_number = message["sequence_number"]

        # Deduplication check
        if message_id in self.processed_ids:
            return "Message already processed"

        # Total order processing
        if sequence_number == self.expected_sequence_number:
            self.append_to_log(sequence_number, message)
            self.expected_sequence_number += 1

            # Check if next messages are waiting in the buffer
            while self.expected_sequence_number in self.out_of_order_messages:
                self.append_to_log(
                    self.expected_sequence_number,
                    self.out_of_order_messages.pop(self.expected_sequence_number),
                )
                self.expected_sequence_number += 1
        else:
            # Store out-of-order messages in a buffer
            self.out_of_order_messages[sequence_number] = message

        return "Message processed"

    def append_to_log(self, sequence_number, message):
        self.message_log[sequence_number] = message
        self.processed_ids.add(message["id"])

    def get_ordered_messages(self):
        # Returns a list of all messages in order of their sequence numbers
        return [self.message_log[seq] for seq in sorted(self.message_log)]
