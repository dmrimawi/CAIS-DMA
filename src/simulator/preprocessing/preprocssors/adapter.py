#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This abstract module is to create an adapter to prepare the data entry in the same
# Structure as the Collaborative AI System under test is 

#####################
#   Native Imports  #
#####################


######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from simulator.preprocessing.preprocssors.color_classification.color_classification_adapter import ColorClassificationAdapter

################
#   CONSTANTS  #
################
COLOR_CLASSIFICATION = "color_classification"


class Adapter():
    def __init__(self) -> None:
        super().__init__()

    def request(self, obj, dataset_name):
        if dataset_name == COLOR_CLASSIFICATION:
            adapter = ColorClassificationAdapter()
            return adapter.request(obj)
        return None
