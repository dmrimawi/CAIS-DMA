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

    def add_acr_to_csv_file(self):
        """
        This method computes the ACR value for the human-system collaboration
        """
        logging.info("Update the ACR values, for time frame of size {}, on the log file {}".format( \
                    self.time_frame_size, self.csv_file))
        data_frame = Common.load_files_pandas(self.csv_file)
        time_frame_queue = self.__init_queue()
        acr_column = list()
        for _, action in data_frame.iterrows():
            time_frame_queue.pop(0)
            if action["Action"] == DMAConstants.AUTONOMOUS:
                time_frame_queue.append(1)
            else:
                time_frame_queue.append(0)
            acr_value = sum(time_frame_queue) / len(time_frame_queue)
            acr_column.append(acr_value)
        data_frame[DMAConstants.CSV_ACR_DUMP_FIELD_NAME] = acr_column
        Common.write_dataframe_to_csv(data_frame, self.csv_file)




        
