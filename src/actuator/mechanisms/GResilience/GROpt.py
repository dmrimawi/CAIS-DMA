#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# Extending CORAL with the GResilience Approach


#####################
#   Native Imports  #
#####################
import os

######################
#   Modules Imports  #
######################
from sklearn import preprocessing
import numpy as np

####################
#   Local Imports  #
####################
from utils.DMALogger import logging
from utils.DMACommon import Common

#################
#   CONSTANTS   #
#################
SMOOTHING_CONSTANT = 0.5
MAX_HUMAN_INTERACTIONS = 12
ACTION_1_ARM = "a1"
ACTION_2_HUMAN = "a2"
PLAYER_RESILIENCE = "Pr"
PLAYER_GREENNESS = "Pg"

class GROpt:
    """
    Hardcoded for two actions (a1): ARM, and (a2): Human
    """
    def __init__(self, actions_data, probabilities):
        """
        The actions_data: are the actions attributes
        actions_data = {"ARMCO2": 0, "ARMTime": 0, "HumCO2": 0, "HumTime": 0, "HumRed": 0, "HumGreen": 0, "HumBlue": 0, \
                        "EstARMCO2": 0, "EstARMTime": 0, "EstHumCO2": 0, "EstHumTime": 0}
        probabilities: are the probability generated for the object class
        probabilities = [0.0, 0.0, 0.0]
        """
        self.actions_data = actions_data
        self.prob = probabilities
        self.target = self.prob.index(max(self.prob)) + 1
        self.object_color = "HumRed"
        if self.target == 2:
            self.object_color = "HumGreen"
        elif self.target == 3:
            self.object_color = "HumBlue"
        self.decision_matrix = {ACTION_1_ARM: {"time": 0, "human": 0, "co2": 0}, \
                                ACTION_2_HUMAN: {"time": 0, "human": 0, "co2": 0}}
        self.weights = {"time": 0.50, "human": 0.50, "co2": 0.50}

    def estimate_next_value(self, prev_value, prev_estimation, environ_key=None):
        """
        Smoothing estimator
        """
        estimation = prev_estimation + SMOOTHING_CONSTANT * (prev_value - prev_estimation)
        if environ_key is not None:
             os.environ[environ_key] = str(estimation)
        return estimation

    def update_estimated_values(self, arm_time, hum_time, arm_co2, hum_co2):
        """
        This method set the new values estimated to the os environemental variables to be shared among the whole app
        """
        os.environ["EstARMTime"] = str(arm_time)
        os.environ["EstHumTime"] = str(hum_time)
        os.environ["EstARMCO2"] = str(arm_co2)
        os.environ["EstHumCO2"] = str(hum_co2)
        return 0

    def init_decision_matrix(self):
        """
        Initiate the decision matrix with the initial values, to be normalized later
        """
        self.decision_matrix[ACTION_1_ARM] = {"time": self.estimate_next_value(self.actions_data.get("ARMTime"), \
                                                                       self.actions_data.get("EstARMTime")), \
                                      "human": MAX_HUMAN_INTERACTIONS - self.actions_data.get(self.object_color), \
                                      "co2": self.estimate_next_value(self.actions_data.get("ARMCO2"), \
                                                                      self.actions_data.get("EstARMCO2"))}
        self.decision_matrix[ACTION_2_HUMAN] = {"time": self.estimate_next_value(self.actions_data.get("HumTime"), \
                                                                       self.actions_data.get("EstHumTime")), \
                                      "human": MAX_HUMAN_INTERACTIONS - self.actions_data.get(self.object_color) - 1, \
                                      "co2": self.estimate_next_value(self.actions_data.get("HumCO2"), \
                                                                      self.actions_data.get("EstHumCO2"))}
        rc = self.update_estimated_values(self.decision_matrix.get(ACTION_1_ARM).get("time"), \
                                          self.decision_matrix.get(ACTION_2_HUMAN).get("time"), \
                                          self.decision_matrix.get(ACTION_1_ARM).get("co2"), \
                                          self.decision_matrix.get(ACTION_2_HUMAN).get("co2"))
        return rc

    def find_inverse(self, x):
        if x != 0:
            return 1 / x
        return x

    def inverse_time_and_co2(self):
        """
        Inverse the time, and CO2 values
        """
        self.decision_matrix[ACTION_1_ARM]["time"] = self.find_inverse(self.decision_matrix[ACTION_1_ARM]["time"])
        self.decision_matrix[ACTION_1_ARM]["co2"] = self.find_inverse(self.decision_matrix[ACTION_1_ARM]["co2"])
        self.decision_matrix[ACTION_2_HUMAN]["time"] = self.find_inverse(self.decision_matrix[ACTION_2_HUMAN]["time"])
        self.decision_matrix[ACTION_2_HUMAN]["co2"] = self.find_inverse(self.decision_matrix[ACTION_2_HUMAN]["co2"])
        return 0

    def normalize_decision_matrix(self):
        """
        Normalize the values of the decision matrix between [0, 1]
        """
        time_values = np.array([self.decision_matrix.get(ACTION_1_ARM).get("time"), self.decision_matrix.get(ACTION_2_HUMAN).get("time")])
        human_values = np.array([self.decision_matrix.get(ACTION_1_ARM).get("human"), self.decision_matrix.get(ACTION_2_HUMAN).get("human")])
        co2_values = np.array([self.decision_matrix.get(ACTION_1_ARM).get("co2"), self.decision_matrix.get(ACTION_2_HUMAN).get("co2")])
        self.decision_matrix[ACTION_1_ARM] = {"time": preprocessing.normalize([time_values])[0][0], \
                                      "human": preprocessing.normalize([human_values])[0][0], \
                                      "co2": preprocessing.normalize([co2_values])[0][0]}
        self.decision_matrix[ACTION_2_HUMAN] = {"time": preprocessing.normalize([time_values])[0][1], \
                                      "human": preprocessing.normalize([human_values])[0][1], \
                                      "co2": preprocessing.normalize([co2_values])[0][1]}
        return 0

    def find_weights_using_ahp(self):
        # TODO: rewrite this function to utalize the AHP method to find the weights
        self.weights = self.weights
        return 0

    def calculate_global_scores(self):
        """
        Find action1 and action2 scores, based on the defined optimization function
        """
        epsilon = max(self.prob)
        self.decision_matrix[ACTION_1_ARM]["score"] = (self.weights["time"] * epsilon * self.decision_matrix[ACTION_1_ARM]["time"]) + \
                                              ((1 - epsilon) * ((self.weights["human"] * self.decision_matrix[ACTION_1_ARM]["human"]) + \
                                                                (self.weights["co2"] * self.decision_matrix[ACTION_1_ARM]["co2"])))
        self.decision_matrix[ACTION_2_HUMAN]["score"] = (self.weights["time"] * epsilon * self.decision_matrix[ACTION_2_HUMAN]["time"]) + \
                                              ((1 - epsilon) * ((self.weights["human"] * self.decision_matrix[ACTION_2_HUMAN]["human"]) + \
                                                                (self.weights["co2"] * self.decision_matrix[ACTION_2_HUMAN]["co2"])))
        return 0

    def find_actions_score(self):
        """
        This method moderates the steps of WSM to find the score of each action
        """
        # Step1: Building the decision Matrix
        logging.info("Step1: decision matrix before init: \n{}".format(Common.from_dict_of_dict_to_table(self.decision_matrix)))
        rc = self.init_decision_matrix()
        rc = self.inverse_time_and_co2() or rc
        logging.info("Step1: decision matrix after init: \n{}".format(Common.from_dict_of_dict_to_table(self.decision_matrix)))
        # Step2: Normalization
        rc = self.normalize_decision_matrix() or rc
        logging.info("Step2: decision matrix Normalization: \n{}".format(Common.from_dict_of_dict_to_table(self.decision_matrix)))
        # Step3: Find the weights
        rc = self.find_weights_using_ahp() or rc
        # Step4: Calculate the global scores
        rc = self.calculate_global_scores() or rc
        logging.info("Step3: decision matrix with scores: \n{}".format(Common.from_dict_of_dict_to_table(self.decision_matrix)))
        return rc

    def action_selection_optimization(self):
        """
        This method returns true if action1 score is more than action2 score
        """
        logging.info("Action1 Score: {}, while Action2: {}".format(self.decision_matrix[ACTION_1_ARM]["score"], \
                                                                   self.decision_matrix[ACTION_2_HUMAN]["score"]))
        return self.decision_matrix[ACTION_1_ARM]["score"] >= self.decision_matrix[ACTION_2_HUMAN]["score"]

    def tradeoff(self):
        """
        This technique follows the steps of WSM and return True, in case action1 (ARM) is selected
        and False otherwise (HUMAN) is selected
        """
        if self.actions_data is None:
            return False
        rc = self.find_actions_score()
        if not rc:
            return self.action_selection_optimization()
        return False
