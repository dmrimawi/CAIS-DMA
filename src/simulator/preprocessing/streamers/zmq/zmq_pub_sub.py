#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This module contains the apis needed to stream a data through zmq

#####################
#   Native Imports  #
#####################
import json
from threading import Thread


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
    def __init__(self, address):
        """
        Initialize the ZeroMQHandler with the given address.

        Parameters:
        - address (str): The address to be used for creating sockets.
        """
        self.address = address
        self.context = zmq.Context()

    def create_publisher(self, port):
        """
        Create and return a PUB socket for publishing messages.

        Parameters:
        - port (int): The port on which the publisher socket will bind.

        Returns:
        - zmq.Socket: The created publisher socket.
        """
        socket = self.context.socket(zmq.PUB)
        socket.bind(f"tcp://{self.address}:{port}")
        return socket

    def create_subscriber(self, port, conflate=True):
        """
        Create and return a SUB socket for subscribing to messages.

        Parameters:
        - port (int): The port on which the subscriber socket will connect.
        - conflate (bool): Enable or disable the conflate feature on the subscriber.

        Returns:
        - zmq.Socket: The created subscriber socket.
        """
        socket = self.context.socket(zmq.SUB)
        socket.connect(f"tcp://{self.address}:{port}")
        if conflate:
            socket.setsockopt(zmq.CONFLATE, 1)  # Enable conflate
        socket.setsockopt_string(zmq.SUBSCRIBE, '')  # Subscribe to all messages
        return socket

    def publish_message(self, publisher_socket, data):
        """
        Publish a message using the given publisher socket.

        Parameters:
        - publisher_socket (zmq.Socket): The publisher socket to use for publishing.
        - data (dict): The data to be published (will be converted to JSON).

        Returns:
        - None
        """
        message = json.dumps(data)
        publisher_socket.send_string(message)

    def receive_message(self, subscriber_socket, process_callback):
        """
        Receive a message using the given subscriber socket and process it using the callback.

        Parameters:
        - subscriber_socket (zmq.Socket): The subscriber socket to use for receiving.
        - process_callback (callable): The callback function to process the received data.

        Returns:
        - None
        """
        message = subscriber_socket.recv(flags=zmq.NOBLOCK).decode("utf-8")
        data = json.loads(message)
        process_callback(data)
