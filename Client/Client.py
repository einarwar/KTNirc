# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # TODO: Finish init process with necessary code
        self.host = host
        self.server_port = server_port
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()
        #pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        message = self.connection.recv(1024)
        #pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.send(data)
        pass

    def encode_payload(self, request, content):
        payload = {'request': request, 'content': content}
        payload = json.dumps(payload)
        return payload

    def create_request(self, command):
        # Sort the commands by length. We assume we only get request,content or request, None
        command_length = len(command.split())
        if command_length == 1:
            content = None
        elif command_length == 2:
            request, content = command.split()
        else:
            return False

        # Error checking to make sure we dont send login without username or logout with a command
        if request == 'login' or 'msg' and content!=None:
            payload = self.encode_payload(request, content)

        elif request == 'logout' or 'names' or 'help' and content == None:
            payload = self.encode_payload(request, content)

        else:
            return False

        return payload

    def send_payload_from_user_input(self):
        command = raw_input('Enter command here: ')
        payload = self.create_request(command)
        self.send_payload(payload)

    # More methods may be needed!




if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
