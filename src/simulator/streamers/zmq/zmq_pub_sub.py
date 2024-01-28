#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This module contains the apis needed to stream a data through zmq

#####################
#   Native Imports  #
#####################
import json
import numpy as np

######################
#   Modules Imports  #
######################
import zmq

####################
#   Local Imports  #
####################


################
#   CONSTANTS  #
################


class ZeroMQHandler:
    def __init__(self):
        """
        Initialize the ZeroMQHandler with the given address.

        Parameters:
        - address (str): The address to be used for creating sockets.
        """
        self.context = zmq.Context()

    def create_publisher(self, address, port):
        """
        Create and return a PUB socket for publishing messages.

        Parameters:
        - port (int): The port on which the publisher socket will bind.

        Returns:
        - zmq.Socket: The created publisher socket.
        """
        socket = self.context.socket(zmq.PUB)
        socket.bind(f"tcp://{address}:{port}")
        return socket

    def create_subscriber(self, address, port):
        """
        Create and return a SUB socket for subscribing to messages.

        Parameters:
        - port (int): The port on which the subscriber socket will connect.
        - conflate (bool): Enable or disable the conflate feature on the subscriber.

        Returns:
        - zmq.Socket: The created subscriber socket.
        """
        socket = self.context.socket(zmq.SUB)
        socket.connect(f"tcp://{address}:{port}")
        socket.setsockopt(zmq.SUBSCRIBE, b"")  # Subscribe to all messages
        socket.setsockopt(zmq.CONFLATE, 1)  # Enable conflate
        return socket

    def convert_to_json_serializable(self, data):
        """
        Recursively convert NumPy int64 objects to regular Python integers.
        """
        if isinstance(data, dict):
            return {key: self.convert_to_json_serializable(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_to_json_serializable(item) for item in data]
        elif isinstance(data, np.int64):
            return int(data)
        else:
            return data

    def publish_message(self, publisher_socket, data):
        """
        Publish a message using the given publisher socket.

        Parameters:
        - publisher_socket (zmq.Socket): The publisher socket to use for publishing.
        - data (dict): The data to be published (will be converted to JSON).

        Returns:
        - None
        """
        data = self.convert_to_json_serializable(data)
        message = json.dumps(data)
        publisher_socket.send_string(message)

    def receive_message(self, subscriber_socket):
        """
        Receive a message using the given subscriber socket and process it using the callback.

        Parameters:
        - subscriber_socket (zmq.Socket): The subscriber socket to use for receiving.

        Returns:
        - None
        """
        message = subscriber_socket.recv(flags=zmq.NOBLOCK).decode("utf-8")
        data = json.loads(message)
        return data

    def terminate_context(self):
        """
        Terminates the context object

        Parameters:
        - None

        Returns:
        - None
        """
        self.context.term()
