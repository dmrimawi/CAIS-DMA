#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# Selecting the action

#####################
#   Native Imports  #
#####################
import json

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from utils.DMALogger import logging
from actuator.actions.color_classification_actions.human_action import HumanAction
from actuator.actions.color_classification_actions.autonomous_action import AutonomousAction

################
#   CONSTANTS  #
################


class ActionSelector():
    def __init__(self, name: str, desc: str, dataset: str, data: str) -> None:
        self.name = name
        self.desc = desc
        self.dataset = dataset
        self.data = data
        logging.info("Selecing an actoin for {}, {}".format(self.name, self.desc))

    def perform_action(self):
        """
        This method runs the action based on the data passed
        """
        operator = None
        if self.data[1]['Detections'][0]['Target'] == -1:
            logging.info("Running a human action to classify the object")
            operator = HumanAction(self.name, self.desc, self.dataset, self.data)
        else:
            logging.info("Running an autonomous action to place the object in the box")
            operator = AutonomousAction(self.name, self.desc, self.dataset, self.data)
        return operator.perform_action()
