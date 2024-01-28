#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This class performs the human action, by classifying the action
# It takes the unclassified data, and update the Target

#####################
#   Native Imports  #
#####################
import os
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


class HumanAction(Action):
    def __init__(self, name: str, desc: str, dataset_file: str, data: str) -> None:
        """
        """
        if desc == '' or desc is None:
            self.desc = """
                            This Action Updates the info of the data based on the Human operator
                        """
        # The data is a json format sent from the mlclassifier
        self.data = data
        self.name = name
        self.dataset_file = dataset_file
        self.__set_action_attributes()
        super().__init__(name, self.desc, dataset_file)

    def __get_human_action_csv(self):
        """
        This method reads the human action csv file and return the content
        """
        csv_file_path = os.path.join(os.path.dirname(self.dataset_file), DMAConstants.CSV_HUMAN_ACTION)
        return Common.load_files_pandas(csv_file_path)

    def __set_action_attributes(self):
        """
        This method set the actions attributes
        """
        human_data = self.__get_human_action_csv()
        self.execution_time = random.choice(human_data[DMAConstants.CSV_COL_ACTION_TIME])
        self.human_interactions_required = 1
        self.co2_footprint = random.choice(human_data[DMAConstants.CSV_COL_ACTION_CO2])

    def perform_action(self):
        """
        This method overrides the perform action method
        """
        # self.data[1]['Detections'][0]['Target'] = 
        obj_id = self.data[1]['Detections'][0]['ObjectID']
        dataset = Common.load_files_pandas(self.dataset_file)
        target = dataset[DMAConstants.CSV_COL_CLASS_TITLE][int(obj_id) - 1]
        self.data[1]['Detections'][0]['Target'] = target
        self.data[1]['ClassificationTime'] = float(self.data[1]['DetectionTime']) + float(self.execution_time)
        self.data[1]['ClassificationCO2'] = self.co2_footprint
        self.data[1]['NHI'] = self.human_interactions_required # NHI (Number of Human Interactions)
        self.data = {'ObjectID': obj_id, 'Target': target, 'Teaching': True, 'ResetModel': False, 'all': self.data}
        logging.info(f"Object {obj_id}, Target {target}, Time {self.execution_time}, CO2 {self.co2_footprint}, " \
                     f"NHI {self.human_interactions_required}")
        return self.data

