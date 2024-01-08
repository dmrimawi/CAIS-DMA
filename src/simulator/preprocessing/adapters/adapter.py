#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This is an abstract class that defines the methods of any adaptor in the framework
# Adaptors are classes that performs data transformation from one structure represented to other
# before being fed to the next step Data Feeder
# IMPORTANT NOTE:
# Please note that all Adaptors should be inside a directory that has the same name as the dataset


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


class Adapter(ABC):
    @abstractmethod
    def __init__(self, name: str, desc: str, dataset_path: str, output_path: str) -> None:
        super().__init__()
        self.name = name
        self.desc = desc
        self.dataset_path = dataset_path
        self.output_path = output_path
        logging.info("Running Disruptor for: {}".format(self.name))
        logging.info("Desciption: {}".format(self.desc))
        logging.info("Dataset: {}".format(self.dataset_path))
        logging.info("Output: {}".format(self.output_path))

    @abstractmethod
    def fetch_dataset(self):
        """
        Fetch the dataset rows
        """
        pass

    @abstractmethod
    def apply(self):
        """
        The request method of the adapter
        """
        pass

    @abstractmethod
    def dump(self):
        """
        Save output
        """
        pass
