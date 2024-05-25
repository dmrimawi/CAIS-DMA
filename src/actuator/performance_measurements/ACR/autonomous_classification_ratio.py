#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This class  takes the current list of actions, then compute the ACR value

#####################
#   Native Imports  #
#####################


######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from utils import DMAConstants
from utils.DMACommon import Common
from utils.DMALogger import logging

################
#   CONSTANTS  #
################
DISRUPTED_MECHANISIME_STATE = DMAConstants.STATES_NAMES[DMAConstants.DISRUPTED_STATE_INDEX]


class ACR():
    def __init__(self, csv_file, time_frame_size=5) -> None:
        """
        csv_file: is the dump file for the human-system collaboration
        """
        self.csv_file = csv_file
        self.time_frame_size = time_frame_size

    def __init_queue(self):
        """
        This creates a queue of size time_frame_size of zero values
        """
        return [0] * self.time_frame_size

    def get_state_name(self, need_mechanism, state_index, acr_value, with_support_queue):
        if state_index == 0 and acr_value == 1:
                state_index = 1
        if state_index == 1 and acr_value == 0:
            state_index = 2
            need_mechanism = True
        elif need_mechanism and sum(with_support_queue) == 0:
            need_mechanism = False
        if state_index > DMAConstants.DISRUPTED_STATE_INDEX:
            need_mechanism = False
        return need_mechanism, state_index, DMAConstants.STATES_NAMES[state_index]

    def evaluate_acr_values(self, update_csv_file=True):
        """
        This method computes the ACR value for the human-system collaboration
        """
        if not update_csv_file and not Common.check_if_file_dir_exists(self.csv_file, is_file=True):
            return False
        logging.info("Update the ACR values, for time frame of size {}, on the log file {}".format( \
                    self.time_frame_size, self.csv_file))
        data_frame = Common.load_files_pandas(self.csv_file)
        time_frame_queue = self.__init_queue()
        with_support_queue = self.__init_queue()
        state_index = 0
        states_names_column = list()
        need_mechanism = False
        mechanism_column = list()
        acr_column = list()
        for _, action in data_frame.iterrows():
            time_frame_queue.pop(0)
            with_support_queue.pop(0)
            if action["Action"] == DMAConstants.AUTONOMOUS:
                time_frame_queue.append(1)
            else:
                time_frame_queue.append(0)
            with_support_queue.append(int(action["WithSupport"]))
            acr_value = sum(time_frame_queue) / len(time_frame_queue)
            acr_column.append(acr_value)
            need_mechanism, state_index, state_name = self.get_state_name(need_mechanism, state_index, acr_value, \
                                                                          with_support_queue)
            mechanism_column.append(need_mechanism)
            states_names_column.append(state_name)
        data_frame[DMAConstants.CSV_ACR_DUMP_FIELD_NAME] = acr_column
        data_frame["State"] = states_names_column
        data_frame["NeedMechanism"] = mechanism_column
        if update_csv_file:
            Common.write_dataframe_to_csv(data_frame, self.csv_file)
        return mechanism_column[-1]
