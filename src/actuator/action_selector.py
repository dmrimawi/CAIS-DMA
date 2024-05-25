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
import numpy as np


####################
#   Local Imports  #
####################
from utils import DMAConstants
from utils.DMACommon import Common
from utils.DMALogger import logging
from actuator.mechanisms.mechanism import Mechanism
from actuator.actions.color_classification_actions.human_action import HumanAction
from actuator.actions.color_classification_actions.autonomous_action import AutonomousAction

################
#   CONSTANTS  #
################


class ActionSelector():
    def __init__(self, name: str, desc: str, dataset: str, data: str, cls_nmbr: int, need_mechanism: bool) -> None:
        self.name = name
        self.desc = desc
        self.dataset = dataset
        self.data = data
        self.csv_dump_log = os.path.join(os.path.dirname(self.dataset), DMAConstants.CSV_FINAL_DUMP)
        self.cls_nmbr = cls_nmbr
        self.human_inter_utalized_color = "HumRed"
        if self.cls_nmbr == 2:
            self.human_inter_utalized_color = "HumGreen"
        elif self.cls_nmbr == 3:
            self.human_inter_utalized_color = "HumBlue"
        self.need_mechanism = need_mechanism
        self.actions_data = {"ARMCO2": 0, "ARMTime": 0, "HumCO2": 0, "HumTime": 0, "HumRed": 0, "HumGreen": 0, "HumBlue": 0, \
                        "EstARMCO2": 0, "EstARMTime": 0, "EstHumCO2": 0, "EstHumTime": 0}
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

    def __init_probs_vars(self):
        predict_prob = self.data[1]['Detections'][0]['PredictProba']
        min_diff, max_diff = self.find_max_min_difference(predict_prob)
        min_val = min(predict_prob)
        max_val = max(predict_prob)
        return predict_prob, min_diff, max_diff, min_val, max_val

    def reset_actions_data_dict(self):
        if Common.check_if_file_dir_exists(self.csv_dump_log, is_file=True):
            dump_log = Common.load_files_pandas(self.csv_dump_log, csv=True)
            last_autonomous_row = None
            last_human_row = None
            autnonmous_actions = dump_log[dump_log['Action'] == DMAConstants.AUTONOMOUS]
            if len(autnonmous_actions) > 0:
                last_autonomous_row = autnonmous_actions.iloc[-1]
                self.actions_data['ARMCO2'] = last_autonomous_row['CO2']
                self.actions_data['ARMTime'] = last_autonomous_row['Time']
                self.actions_data["EstARMCO2"] = last_autonomous_row["EstARMCO2"]
                self.actions_data["EstARMTime"] = last_autonomous_row["EstARMTime"]
            human_actions = dump_log[dump_log['Action'] == DMAConstants.HUMAN]
            if len(human_actions) > 0:
                last_human_row = human_actions.iloc[-1]
                self.actions_data['HumCO2'] = last_human_row['CO2']
                self.actions_data['HumTime'] = last_human_row['Time']
                self.actions_data["EstHumCO2"] = last_human_row["EstHumCO2"]
                self.actions_data["EstHumTime"] = last_human_row["EstHumTime"]
            last_row = dump_log.iloc[-1]
            self.actions_data["HumRed"] = last_row["HumRed"]
            self.actions_data["HumGreen"] = last_row["HumGreen"]
            self.actions_data["HumBlue"] = last_row["HumBlue"]

    def apply_support_mechanism(self, predict_prob):
        """
        This method return the action operator based on the mechanism
        if action is True -> ARM, else -> Human
        """
        mechanism = Mechanism.create_mechanism(DMAConstants.SELECTED_MECHANISM, \
                                                self.actions_data, \
                                                predict_prob)
        action = mechanism.tradeoff()
        self.actions_data["EstARMCO2"] = float(os.environ.get("EstARMCO2", '0'))
        self.actions_data["EstARMTime"] = float(os.environ.get("EstARMTime", '0'))
        self.actions_data["EstHumCO2"] = float(os.environ.get("EstHumCO2", '0'))
        self.actions_data["EstHumTime"] = float(os.environ.get("EstHumTime", '0'))
        if not action:
            self.actions_data[self.human_inter_utalized_color] = self.actions_data[self.human_inter_utalized_color] + 1
        return action

    def convert_bools(self, obj):
        if isinstance(obj, dict):
            return {k: self.convert_bools(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_bools(item) for item in obj]
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return obj        

    def get_operator_info(self, predict_prob, supported_action_decision, operator_name):
        if self.data[1]['Detections'][0]['Target'] == -1 and \
            (supported_action_decision is None or not supported_action_decision):
            logging.info("Running a human action to classify the object")
            operator = HumanAction(self.name, self.desc, self.dataset, self.data)
            operator_name = DMAConstants.HUMAN
        else:
            logging.info("Running an autonomous action to place the object in the box")
            operator = AutonomousAction(self.name, self.desc, self.dataset, self.data)
            if supported_action_decision:
                max_prob_indx = max(enumerate(predict_prob), key=lambda x: x[1])[0]
                self.data[1]['Detections'][0]['Target'] = max_prob_indx + 1
        return operator, operator_name

    def write_to_csv_dump(self, predict_prob, min_diff, max_diff, min_val, max_val, with_support, \
                          operator, operator_name, action_data):
        header = DMAConstants.CSV_FINAL_DUMP_HEADERS
        if Common.check_if_file_dir_exists(self.csv_dump_log, is_file=True):
            header = None
        misclassification = 0
        if self.cls_nmbr == int(action_data['Target']):
            misclassification = 1
        object_type = self.data[1]['Detections'][0]['ObjectType']
        data_to_dump = [action_data['ObjectID'], operator_name, with_support, action_data['Target'], \
                        operator.human_interactions_required, operator.co2_footprint, \
                        operator.execution_time, misclassification, predict_prob, \
                        max_val, min_val, max_diff, min_diff, object_type] + \
                        [self.actions_data["HumRed"], self.actions_data["HumGreen"], self.actions_data["HumBlue"], \
                         self.actions_data["EstARMCO2"], self.actions_data["EstARMTime"], self.actions_data["EstHumCO2"], \
                         self.actions_data["EstHumTime"]]
        action_data = self.convert_bools(action_data)
        Common.write_to_csv(data=data_to_dump, filename=self.csv_dump_log, header=header)
        return action_data

    def perform_action(self):
        """
        This method runs the action based on the data passed
        """
        predict_prob, min_diff, max_diff, min_val, max_val = self.__init_probs_vars()
        print(f"The max prob: {max_val}, comparing to K: {DMAConstants.VALUE_OF_DESIRED_TRUST_LEVEL}")
        print(f"The system needs mechanism? {self.need_mechanism}")
        with_support = 0
        supported_action_decision = None
        self.reset_actions_data_dict()
        if max_val < DMAConstants.VALUE_OF_DESIRED_TRUST_LEVEL:
            with_support = 1
            if DMAConstants.SELECTED_MECHANISM.lower() != DMAConstants.INTERNAL_MECHANISM.lower() \
                and self.need_mechanism:
                supported_action_decision = self.apply_support_mechanism(predict_prob)
        operator = None
        operator_name = DMAConstants.AUTONOMOUS
        operator, operator_name = self.get_operator_info(predict_prob, supported_action_decision, operator_name)
        action_data = operator.perform_action()
        if supported_action_decision:
            action_data["Teaching"] = supported_action_decision
        action_data = self.write_to_csv_dump(predict_prob, min_diff, max_diff, min_val, max_val, \
                                             with_support, operator, operator_name, action_data)
        logging.info({key: value for key, value in action_data.items() if key != 'all'})
        return action_data
