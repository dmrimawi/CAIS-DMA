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
from utils import DMAConstants
from utils.DMALogger import logging
from utils.DMACommon import Common


#################
#   CONSTANTS   #
#################
MAX_HUMAN_INTERACTIONS = 12
ACTION_1_ARM = "a1"
ACTION_1_ARM_INDX = 0
ACTION_2_HUMAN = "a2"
PLAYER_RESILIENCE = "Pr"
PLAYER_GREENNESS = "Pg"
MSNE = "msne"

class GRGame:
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
        self.game_payoffs = {PLAYER_RESILIENCE: {ACTION_1_ARM: [0, 0], ACTION_2_HUMAN: [0, 0]}, \
                             PLAYER_GREENNESS: {ACTION_1_ARM: [0, 0], ACTION_2_HUMAN: [0, 0]}}
        self.resilience_payoffs = list()
        self.greenness_payoffs = list()
        self.segmas = {PLAYER_RESILIENCE: 0, PLAYER_GREENNESS: 0}
        os.environ["GRresilience_INIT"] = str(1)

    def find_inverse(self, x):
        if x != 0:
            return 1 / x
        return x

    def estimate_next_value(self, prev_value, prev_estimation, environ_key=None):
        """
        Smoothing estimator
        """
        estimation = prev_estimation + DMAConstants.SMOOTHING_CONSTANT * (prev_value - prev_estimation)
        if environ_key is not None:
             os.environ[environ_key] = str(estimation)
        return estimation

    def get_resilience_payoff(self, epsilon, alpha, player_action):
        """
        For player resilience this function calculates the payoff, based on epsilon and alpha
        and the choosen action
        """
        action_time_key = "ARMTime"
        action_est_time_key = "EstARMTime"
        if player_action == ACTION_2_HUMAN:
            action_time_key = "HumTime"
            action_est_time_key = "EstHumTime"
        est_inv_time = self.find_inverse(self.estimate_next_value(self.actions_data.get(action_time_key), \
                                                                  self.actions_data.get(action_est_time_key), \
                                                                  environ_key=action_est_time_key))
        return epsilon * alpha * est_inv_time

    def get_greenness_payoff(self, epsilon, alpha, player_action):
        """
        For player greenness this function calculates the payoff, based on epsilon and alph
        and the choosen action
        """
        action_co2_key = "ARMCO2"
        action_est_co2_key = "EstARMCO2"
        if player_action == ACTION_2_HUMAN:
            action_co2_key = "HumCO2"
            action_est_co2_key = "EstHumCO2"
        est_inv_co2 = self.find_inverse(self.estimate_next_value(self.actions_data.get(action_co2_key), \
                                                                 self.actions_data.get(action_est_co2_key), \
                                                                 environ_key=action_est_co2_key))
        interactions_required = (0, 1)[player_action == ACTION_2_HUMAN]
        human_inv_inter = self.find_inverse(MAX_HUMAN_INTERACTIONS \
                                            - interactions_required \
                                            - self.actions_data.get(self.object_color))
        return (1 - epsilon) * alpha * human_inv_inter * est_inv_co2

    def get_payoff(self, player, player_action, scond_player_action):
        """
        Find the player payoff for the selected actions
        """
        epsilon = max(self.prob)
        alpha = (1, 2)[player_action == scond_player_action]
        payoff = 0
        if player == PLAYER_RESILIENCE:
            payoff = self.get_resilience_payoff(epsilon, alpha, player_action)
        else:
            payoff = self.get_greenness_payoff(epsilon, alpha, player_action)
        return payoff

    def create_the_gresilience_game(self):
        """
        This method initiate the gresilience game with players payoffs
        """
        self.game_payoffs = {
                PLAYER_RESILIENCE: {
                        ACTION_1_ARM: [self.get_payoff(PLAYER_RESILIENCE, ACTION_1_ARM, ACTION_1_ARM), \
                                       self.get_payoff(PLAYER_RESILIENCE, ACTION_1_ARM, ACTION_2_HUMAN)],
                        ACTION_2_HUMAN: [self.get_payoff(PLAYER_RESILIENCE, ACTION_2_HUMAN, ACTION_1_ARM), \
                                         self.get_payoff(PLAYER_RESILIENCE, ACTION_2_HUMAN, ACTION_2_HUMAN)],
                    },
                PLAYER_GREENNESS: {
                        ACTION_1_ARM: [self.get_payoff(PLAYER_GREENNESS, ACTION_1_ARM, ACTION_1_ARM), \
                                       self.get_payoff(PLAYER_GREENNESS, ACTION_1_ARM, ACTION_2_HUMAN)],
                        ACTION_2_HUMAN: [self.get_payoff(PLAYER_GREENNESS, ACTION_2_HUMAN, ACTION_1_ARM), \
                                         self.get_payoff(PLAYER_GREENNESS, ACTION_2_HUMAN, ACTION_2_HUMAN)]
                    }
            }
        return 0

    def normalize_payoff(self):
        """
        This method normalize the payoffs in the gresilience game
        """
        self.resilience_payoffs = list(preprocessing.normalize([np.array([
            self.game_payoffs[PLAYER_RESILIENCE][ACTION_1_ARM][0], \
            self.game_payoffs[PLAYER_RESILIENCE][ACTION_1_ARM][1], \
            self.game_payoffs[PLAYER_RESILIENCE][ACTION_2_HUMAN][0], \
            self.game_payoffs[PLAYER_RESILIENCE][ACTION_2_HUMAN][1]])]).flatten())
        self.greenness_payoffs = list(preprocessing.normalize([np.array([
            self.game_payoffs[PLAYER_GREENNESS][ACTION_1_ARM][0], \
            self.game_payoffs[PLAYER_GREENNESS][ACTION_2_HUMAN][0], \
            self.game_payoffs[PLAYER_GREENNESS][ACTION_1_ARM][1], \
            self.game_payoffs[PLAYER_GREENNESS][ACTION_2_HUMAN][1]])]).flatten())
        self.game_payoffs = {
                PLAYER_RESILIENCE: {
                        ACTION_1_ARM: [self.resilience_payoffs[0], self.resilience_payoffs[1]],
                        ACTION_2_HUMAN: [self.resilience_payoffs[2], self.resilience_payoffs[3]]
                    },
                PLAYER_GREENNESS: {
                        ACTION_1_ARM: [self.greenness_payoffs[0], self.greenness_payoffs[2]],
                        ACTION_2_HUMAN: [self.greenness_payoffs[1], self.greenness_payoffs[3]]
                    }
            }
        return 0

    def find_segmas(self):
        """
        This method finds the segma values (The propabilities of the players for the mixed nash equileprium)
        """
        self.segmas[PLAYER_RESILIENCE] = ((self.game_payoffs[PLAYER_GREENNESS][ACTION_2_HUMAN][1] \
                                       - self.game_payoffs[PLAYER_GREENNESS][ACTION_1_ARM][1]) \
                                       / (self.game_payoffs[PLAYER_GREENNESS][ACTION_2_HUMAN][1] \
                                          + self.game_payoffs[PLAYER_GREENNESS][ACTION_1_ARM][0] \
                                          - self.game_payoffs[PLAYER_GREENNESS][ACTION_1_ARM][1] \
                                          - self.game_payoffs[PLAYER_GREENNESS][ACTION_2_HUMAN][0]))
        self.segmas[PLAYER_GREENNESS] = ((self.game_payoffs[PLAYER_RESILIENCE][ACTION_2_HUMAN][1] \
                                        - self.game_payoffs[PLAYER_RESILIENCE][ACTION_1_ARM][1]) \
                                        / (self.game_payoffs[PLAYER_RESILIENCE][ACTION_1_ARM][0] \
                                          + self.game_payoffs[PLAYER_RESILIENCE][ACTION_2_HUMAN][1] \
                                          - self.game_payoffs[PLAYER_RESILIENCE][ACTION_1_ARM][1] \
                                          - self.game_payoffs[PLAYER_RESILIENCE][ACTION_2_HUMAN][0]))
        if self.segmas[PLAYER_GREENNESS] < 0 or self.segmas[PLAYER_GREENNESS] > 1:
            self.segmas[PLAYER_GREENNESS] = 1
        if self.segmas[PLAYER_RESILIENCE] < 0 or self.segmas[PLAYER_RESILIENCE] > 1:
            self.segmas[PLAYER_RESILIENCE] = 1
        return 0

    def find_msne_payoffs(self):
        """
        Thie method returns the game payoffs matrix with the MSNE payoffs
        """
        res_comp = 1 - self.segmas[PLAYER_RESILIENCE]
        if self.segmas[PLAYER_RESILIENCE] == 1:
            res_comp = 1
        gre_comp = 1 - self.segmas[PLAYER_GREENNESS]
        if self.segmas[PLAYER_GREENNESS] == 1:
            gre_comp = 1
        self.msne_props = [
            self.segmas[PLAYER_RESILIENCE] * self.segmas[PLAYER_GREENNESS],
            self.segmas[PLAYER_RESILIENCE] * gre_comp,
            self.segmas[PLAYER_GREENNESS] * res_comp,
            gre_comp * res_comp
        ]
        resilience = 0
        greenness = 0
        for i in range(len(self.resilience_payoffs)):
            resilience = resilience + self.msne_props[i] * self.resilience_payoffs[i]
            greenness = greenness + self.msne_props[i] * self.greenness_payoffs[i]
        self.game_payoffs[PLAYER_RESILIENCE][MSNE] = resilience
        self.game_payoffs[PLAYER_GREENNESS][MSNE] = greenness
        return 0
    
    def find_psne(self):
        """
        This methods find the pure strategies nash equilprum
        """
        self.matrix = [
            [
                [self.resilience_payoffs[0], self.greenness_payoffs[0], 0], [self.resilience_payoffs[1], self.greenness_payoffs[1], 0]
            ],
            [
                [self.resilience_payoffs[2], self.greenness_payoffs[2], 0], [self.resilience_payoffs[3], self.greenness_payoffs[3], 0]
            ]
        ]
        row1 = self.matrix[0]
        maximum1 = max(row1[0][0], row1[1][0])
        if maximum1 in row1[0]:
            self.matrix[0][0][2] = self.matrix[0][0][2] + 1
        else:
            self.matrix[0][1][2] = self.matrix[0][1][2] + 1
        row2 = self.matrix[1]
        maximum2 = max(row2[0][0], row2[1][0])
        if maximum2 in row2[0]:
            self.matrix[1][0][2] = self.matrix[1][0][2] + 1
        else:
            self.matrix[1][1][2] = self.matrix[1][1][2] + 1
        maximum3 = max(row1[0][1], row2[0][1])
        if maximum3 in row1[0]:
            self.matrix[0][0][2] = self.matrix[0][0][2] + 1
        else:
            self.matrix[1][0][2] = self.matrix[1][0][2] + 1
        maximum4 = max(row1[1][1], row2[1][1])
        if maximum4 in row1[1]:
            self.matrix[0][1][2] = self.matrix[0][1][2] + 1
        else:
            self.matrix[1][1][2] = self.matrix[1][1][2] + 1
        self.pure = []
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                if row[j][2] > 1:
                    t = (i, j)
                    self.pure.append(t)
        return 0

    def play_the_gresilience_game(self):
        # Step1: initiate the game matrix
        rc = self.create_the_gresilience_game()
        logging.info("Step1: The GResilience Game Payoff Matrix: {}".format( \
            Common.from_dict_of_dict_to_table(self.game_payoffs)))
        # Step2: Normalize the game payoffs
        rc = self.normalize_payoff() or rc
        logging.info("Step2: The GResilience Game Normalized Payoff Matrix: {}".format( \
            Common.from_dict_of_dict_to_table(self.game_payoffs)))
        # Step3: find propabilities
        rc = self.find_segmas() or rc
        logging.info("Step3: Segmas are: {}".format(self.segmas))
        # Step4: Calculate the the mixed strategy nash equilbria MSNE payoffs
        rc = self.find_msne_payoffs() or rc
        logging.info("Step4: MSNE are: {}".format( \
            Common.from_dict_of_dict_to_table(self.game_payoffs)))
        # Step5: Find PSNE
        rc = self.find_psne() or rc
        logging.info("Step5: PURE SNE: {}".format(self.pure))
        return rc

    def select_action_gt(self, action_indx):
        """
        return the action to be selected
        """
        if action_indx[ACTION_1_ARM_INDX] == ACTION_1_ARM_INDX:
            return True # Select action1, by ARM
        return False # Select action2

    def get_index(self, indx, max_col):
        """
        For any flattened array, this funcion return the row, col for 2 dimention array of row len of max_col
        """
        if type(indx) == tuple:
            row = 0
            col = indx[0] * max_col + indx[1]
        else:
            row = int(indx / max_col)
            col = indx % max_col
        return row, col

    def check_if_mnse_props_are_same(self):
        """
        This method checks if any of the mnse_prob of the pure equiliprium has a max prob
        """
        prev_pure = self.pure[0]
        for pure_strategy in self.pure:
            _, prev_indx = self.get_index(prev_pure, 2)
            _, prev_stra = self.get_index(pure_strategy, 2)
            if self.msne_props[prev_indx] != self.msne_props[prev_stra]:
                return False
        return True

    def get_pure_with_max_sum(self):
        """
        This method returns the pure equiliprium with the max value
        """
        max_indx = self.pure[0]
        for pure_strategy in self.pure:
            if sum(self.matrix[max_indx[0]][max_indx[1]]) < sum(self.matrix[pure_strategy[0]][pure_strategy[1]]):
                max_indx = pure_strategy
        return max_indx

    def action_selection_game_theory(self):
        """
        This mehtod coordinate the decision making for game theory
        """
        if len(self.pure) == 1:
            logging.info("Only one pure nash to select: {}".format(self.pure[0]))
            return self.select_action_gt(self.pure[0])
        if self.check_if_mnse_props_are_same():
            max_indx = self.get_pure_with_max_sum()
            logging.info("The mnse props are equal, selecing the maximum sum")
            return self.select_action_gt(max_indx)
        i, j = self.get_index(self.msne_props.index(max(self.msne_props)), 2)
        if (i, j) in self.pure:
            logging.info("Select the following action: {}, {}".format(i, j))
            return self.select_action_gt((i, j))
        logging.info("Didn't find a solution: {}, {}".format(i, j))
        return False

    def tradeoff(self):
        """
        This technique follows the steps of the gresilience game and return True, in case action1 (ARM)
        is selected and False otherwise (HUMAN) is selected
        """
        if self.actions_data is None:
            return False
        rc = self.play_the_gresilience_game()
        if not rc:
            return self.action_selection_game_theory()
        return False
