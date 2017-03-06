# -*- coding: utf-8 -*-
import SocketServer
import json
import time
import re
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """



    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.users = []
        self.isLoggedIn = False
        self.username = None
        # Loop that listens for messages from the client
        while True:
            print 'Users connected: {}'.format(self.users)
            received_string = self.connection.recv(4096)
            if received_string:
                decoded_string = json.loads(received_string)
            print decoded_string

            user_request = decoded_string['request']
            user_content = decoded_string['content']
            self.timestamp = time.ctime()
            self.sender = 'Server'

            if user_request == 'login':
                self.handle_user_login(user_content)

            elif user_request == 'logout':
                self.handle_user_logout()

            elif user_request == 'msg':
                self.handle_user_msg(user_content)

            else:
                self.response = 'error'
                self.content = 'Unknown request'


            return_message = {'timestamp': self.timestamp,
                        'sender': self.sender,
                        'response': self.response,
                        'content': self.content}
            self.connection.send(json.dumps(return_message))
            # TODO: Add handling of received payload from client

    def handle_user_login(self, username):
        if self.isLoggedIn:
            self.response = 'error'
            self.content = 'Already logged in'

        elif username is 'None':
            self.response = 'error'
            self.content = 'No username given'

        elif re.match('[a-zA-Z\d]+$', username) is not None:
            if username not in self.users:
                self.users.append(username)
                self.username = username
                self.isLoggedIn = True
                self.response = 'info'
                self.content = 'Login successfull'
            else:
                self.response = 'error'
                self.content = 'Username already taken'
        else:
            self.response = 'error'
            self.content = 'Username not accepted'

    def handle_user_logout(self):
        if self.isLoggedIn:
            self.isLoggedIn = False
            self.users.remove(self.username)
            self.username = None
            self.response = 'info'
            self.content = 'Logout successful'
        else:
            self.response = 'error'
            self.content = 'You are not logged in'

    def handle_user_msg(self, message):
        if self.isLoggedIn:
            self.response = 'message'
            if message == None:
                self.content = ''
            else:
                self.content = message
            self.sender = self.username
        else:
            self.response = 'error'
            self.content = 'You are not logged in'

    def handle_user_history(self):
        pass

    def handle_user_help(self):
        pass


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    SocketServer.TCPServer.allow_reuse_address = True

    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
