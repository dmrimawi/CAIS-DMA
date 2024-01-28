#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This class performs the autonomous action, by classifying the action

#####################
#   Native Imports  #
#####################
import os
import json
import random

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from utils import DMAConstants
from utils.DMACommon import Common
from utils.DMALogger import logging
from actuator.actions.action import Action

################
#   CONSTANTS  #
################


class AutonomousAction(Action):
    def __init__(self, name: str, desc: str, dataset_file: str, data: str) -> None:
        """
        """
        if desc == '' or desc is None:
            self.desc = """
                            This Action Updates the info of the data based on the ARM operator
                        """
        # The data is a json format sent from the mlclassifier
        self.data = data
        self.name = name
        self.dataset_file = dataset_file
        self.__set_action_attributes()
        super().__init__(name, self.desc, dataset_file)

    def __get_autonomous_action_csv(self):
        """
        This method reads the autonomous action csv file and return the content
        """
        csv_file_path = os.path.join(os.path.dirname(self.dataset_file), DMAConstants.CSV_AUTONOMOUS_ACTION)
        return Common.load_files_pandas(csv_file_path)

    def __set_action_attributes(self):
        """
        This method set the actions attributes
        """
        autonomous_data = self.__get_autonomous_action_csv()
        self.execution_time = random.choice(autonomous_data[DMAConstants.CSV_COL_ACTION_TIME])
        self.human_interactions_required  = 0
        self.co2_footprint = random.choice(autonomous_data[DMAConstants.CSV_COL_ACTION_CO2])

    def perform_action(self):
        """
        This method overrides the perform action method
        """
        self.data[1]['ClassificationTime'] = float(self.data[1]['DetectionTime']) + float(self.execution_time)
        self.data[1]['ClassificationCO2'] = self.co2_footprint
        self.data[1]['NHI'] = self.human_interactions_required  # NHI (Number of autonomous Interactions)
        obj_id = self.data[1]['Detections'][0]['ObjectID']
        target = self.data[1]['Detections'][0]['Target']
        self.data = {'ObjectID': obj_id, 'Target': target, 'Teaching': False, 'ResetModel': False, 'all': self.data}
        logging.info(f"Object {obj_id}, Target {target}, Time {self.execution_time}, CO2 {self.co2_footprint}, " \
                     f"NHI {self.human_interactions_required}")
        return self.data

