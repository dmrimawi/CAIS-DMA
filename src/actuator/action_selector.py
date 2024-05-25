#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# Selecting the action

#####################
#   Native Imports  #
#####################
import os

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from utils import DMAConstants
from utils.DMACommon import Common
from utils.DMALogger import logging
from actuator.actions.color_classification_actions.human_action import HumanAction
from actuator.actions.color_classification_actions.autonomous_action import AutonomousAction

################
#   CONSTANTS  #
################


class ActionSelector():
    def __init__(self, name: str, desc: str, dataset: str, data: str, cls_nmbr: int) -> None:
        self.name = name
        self.desc = desc
        self.dataset = dataset
        self.data = data
        self.csv_dump_log = os.path.join(os.path.dirname(self.dataset), DMAConstants.CSV_FINAL_DUMP)
        self.cls_nmbr = cls_nmbr
        # ['ObjectID', 'Action', 'Target', 'HumanInteractions', 'CO2', 'Time']
        logging.info("Selecing an actoin for {}, {}".format(self.name, self.desc))

    def find_max_min_difference(self, items):
        if len(items) < 2:
            return None, None
        
        items.sort()
        
        min_diff = float('inf')
        max_diff = float('-inf')
        
        for i in range(len(items) - 1):
            diff = items[i+1] - items[i]
            min_diff = min(min_diff, diff)
            max_diff = max(max_diff, diff)
        
        return min_diff, max_diff
        

    def perform_action(self):
        """
        This method runs the action based on the data passed
        """
        operator = None
        operator_name = DMAConstants.AUTONOMOUS
        if self.data[1]['Detections'][0]['Target'] == -1:
            logging.info("Running a human action to classify the object")
            operator = HumanAction(self.name, self.desc, self.dataset, self.data)
            operator_name = DMAConstants.HUMAN
        else:
            logging.info("Running an autonomous action to place the object in the box")
            operator = AutonomousAction(self.name, self.desc, self.dataset, self.data)
        action_data = operator.perform_action()
        header = DMAConstants.CSV_FINAL_DUMP_HEADERS
        if Common.check_if_file_dir_exists(self.csv_dump_log, is_file=True):
            header = None
        misclassification = 0
        if self.cls_nmbr == int(action_data['Target']):
            misclassification = 1
        predict_prob = self.data[1]['Detections'][0]['PredictProba']
        min_diff, max_diff = self.find_max_min_difference(predict_prob)
        min_val = min(predict_prob)
        max_val = max(predict_prob)
        object_type = self.data[1]['Detections'][0]['ObjectType']
        data_to_dump = [action_data['ObjectID'], operator_name, action_data['Target'], \
                        operator.human_interactions_required, operator.co2_footprint, \
                        operator.execution_time, misclassification, predict_prob, \
                        max_val, min_val, max_diff, min_diff, object_type]
        Common.write_to_csv(data=data_to_dump, filename=self.csv_dump_log, header=header)
        return action_data
