#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This class converts the provided image to a JSON structure
# As CORAL classifier takes the data

#####################
#   Native Imports  #
#####################
import os

######################
#   Modules Imports  #
######################
import cv2 as cv

####################
#   Local Imports  #
####################
from utils.Exceptions.DMAException import DMAException
from utils.DMACommon import Common
from utils import DMAConstants
from simulator.preprocessing.adapters.adapter import Adapter

################
#   CONSTANTS  #
################


class ColorClassificationAdapter(Adapter):
    def __init__(self, name: str, desc: str, dataset_path: str, output_path: str) -> None:
        """
        This Adaptor convert the object passed (image) to a JSON format as the MLClassifier expects
        """
        if desc == '' or desc is None:
            self.desc = """
                            This Disruptor Adaptor convert the object passed (image)
                            to a JSON format as the MLClassifier expects
                        """.format(self.ratio)
        super().__init__(name, desc, dataset_path, output_path)

    def get_json_example(self):
        """
        This method creates an empty dictionary of CORAL JSON format
        """
        

    def request(self):
        """
        This method is specifc for the color classification adapter of Demo CORAL
        """
        
        return None
