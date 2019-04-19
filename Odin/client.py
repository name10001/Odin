import flask_server as fs
from flask import *
from time import time


class Client:
    def __init__(self, sid, waiting_room):
        self.sid = sid
        self.waiting_room = waiting_room
        self.connected = True

    def send_message(self, message_type, data):
        """
        Sends a message to the client
        :param message_type:
        :param data:
        :return:
        """
        with fs.app.app_context():
            fs.socket_io.emit(message_type, data, room=self.sid)

    def give_message(self, message_type, data):
        """
        When a client sends a message to the back-end, it should come here to be processed
        :param message_type: the type of message sent to the server, e.g. "pickup" or "uno"
        :param data: data that gone along with it, e.g. message="play card", data=("swap_hand_card_15", "Jeff").
        This is not always used.
        :return: None
        """
        # idk what to do here
        pass

    def is_connected(self):
        """
        Is the user currently connected to the back-end with socket-io
        :return:
        """
        return self.connected

    def get_sid(self):
        return sid
