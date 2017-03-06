class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message' : self.parse_message,
            'history' : self.parse_history
	    # More key:values pairs are needed
        }


    def parse(self, payload):
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return 'Response not valid'
            # Response not valid

    def parse_error(self, payload):
        return '[{}] ({}) ERROR: {}'.format(payload['timestamp'], payload['sender'], payload['content'])
    def parse_info(self, payload):
        return '[{}] ({}) INFO: {}'.format(payload['timestamp'], payload['sender'], payload['content'])
    def parse_message(self, payload):
        return '[{}] ({}) MESSAGE: {}'.format(payload['timestamp'], payload['sender'], payload['content'])
    def parse_history(self, payload):
        return '[{}] ({}) HISTORY: {}'.format(payload['timestamp'], payload['sender'], payload['content'])

    # Include more methods for handling the different responses...
