#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This is an abstract class that defines the methods of any Action

#####################
#   Native Imports  #
#####################
from abc import ABC, abstractmethod

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from utils.DMALogger import logging

################
#   CONSTANTS  #
################


class Action(ABC):

    @abstractmethod
    def __init__(self, name: str, desc: str, dataset_file: str) -> None:
        """
        The Disruptor constructors, should pass:
        name: the experiment name
        desc: the Disruptor desciption, e.g. the fade Disruptor generate a faded version of the image
        dataset: is a path to the dataset file (csv)
        """
        super().__init__()
        self.name = name
        self.desc = desc
        self.dataset_file = dataset_file
        logging.info("Running Action for: {}".format(self.name))
        logging.info("Desciption: {}".format(self.desc))
        logging.info("Dataset: {}".format(self.dataset_file))

    @abstractmethod
    def perform_action(self):
        """
        Fetch the dataset rows
        """
        pass
