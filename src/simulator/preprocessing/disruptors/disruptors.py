#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This is an abstract class that defines the methods of any Disruptor in the framework
# Disruptors are classes that performs filters, normalizations, and other data preperation
# before being fed to the next step (disruptors)
# IMPORTANT NOTE:
# Please note that all Disruptors should be inside a directory that has the same name as the dataset

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


class Disruptor(ABC):

    @abstractmethod
    def __init__(self, name: str, desc: str, dataset_path: str, output_path: str) -> None:
        """
        The Disruptor constructors, should pass:
        name: the experiment name
        desc: the Disruptor desciption, e.g. the fade Disruptor generate a faded version of the image
        dataset_path: is a path to the dataset folder (absulute paths)
        """
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
        Calls the private methods for the Disruptor, which updates the raw data with this Disruptor filters
        """
        pass

    @abstractmethod
    def dump(self):
        """
        Dump the new features to JSON file, the JSON formate is:
        {
            0: {
                orignal: pointer to the original data row,
                updated: the new raw data after apply the Disruptor,
            },
        }
        """
        pass
