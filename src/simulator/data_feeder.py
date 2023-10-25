#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This module orchestrate applying preprocessors and disruptors 

#####################
#   Native Imports  #
#####################
import os
import math

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from simulator.preprocessing.disruptors.disruptors_factory import DisruptorsFactory
from utils.DMALogger import logging
from utils.DMACommon import Common
from utils import DMAConstants

################
#   CONSTANTS  #
################


class DataFeeder():
    def __init__(self, name: str, dataset_path: str, output_path: str, csv_file:str, \
                 split_rate: float, adapters=[], disruptors=[]):
        """
        Data Feeder Constructor
        """
        self.name = name
        self.desc = ''
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.csv_file = csv_file
        self.split_rate = split_rate
        self.adapters = adapters
        self.disruptors = disruptors
        self.data_frame = None

    def __apply(self, obj):
        """
        Call the disruptors methods
        """
        obj.fetch_dataset()
        obj.apply()
        obj.dump()

    def __disruptors(self):
        """
        This method responsible to apply the data changes from the selected disruptors
        """
        logging.info("Running disruptors: {}".format(self.disruptors))
        dis_factory = DisruptorsFactory(self.disruptors, self.name, self.desc, self.dataset_path, \
                                           self.output_path)
        while dis_factory.has_next():
            pre_obj = dis_factory.next()
            self.__apply(pre_obj)

    def __adapters(self):
        """
        This method responsible to convert data structure using the adapter
        """
        logging.info("Running Adapters: {}".format(self.disruptors))
        adaptor_factory = None # TODO: Create a disruptors factory object
        # while dis_factory.has_next():
        #     dis_obj = dis_factory.next()
        #     self.__apply(dis_obj)
        pass
    
    def __change_to_disrupted_per_group(self, groups, num):
        """
        This method loops over the groups and change the disrupted column from 0 to 1
        """
        for group in groups.indices.keys():
            num_to_change = num
            if num > len(groups.get_group(group)):
                num_to_change = len(groups.get_group(group))
            for index in groups.get_group(group).sample(n=num_to_change).index:
                self.data_frame.at[index, DMAConstants.DISRUPTED_COL_TITLE] = 1

    def __pick_data_to_disrupt(self):
        """
        This method creats a new column called disrupted (0, 1).
        In the dataframe, all raws with 1 value, will be selected to apply the disruptors on
        """
        if self.data_frame is not None:
            self.data_frame[DMAConstants.DISRUPTED_COL_TITLE] = 0
            length_of_data = len(self.data_frame)
            number_of_items_to_disrupt = math.floor(length_of_data * (self.split_rate / 100.0))
            groups = self.data_frame.groupby(DMAConstants.CSV_COL_CLASS_TITLE)
            number_of_groups = len(groups)
            number_of_items_to_disrupt_per_group = math.floor(number_of_items_to_disrupt / number_of_groups)
            self.__change_to_disrupted_per_group(groups, number_of_items_to_disrupt_per_group)
            Common.save_pandas_df_to_file(self.data_frame, os.path.join(self.output_path, self.csv_file))

    def __prepare_data(self):
        """
        This method perform preprocessing, and disruption over the data, and prepare it
        """
        if len(self.disruptors):
            self.__disruptors()

    def __pre_run(self):
        """
        Common pre running preperations
        """
        self.dataset_name = os.path.basename(self.dataset_path)
        workspace_path = os.path.join(self.output_path, self.dataset_name)
        Common.copy_directory(self.dataset_path, workspace_path)
        self.dataset_path = workspace_path
        self.output_path = workspace_path
        self.data_frame = Common.load_files_pandas(os.path.join(self.output_path, self.csv_file))
        self.__pick_data_to_disrupt()
        self.__prepare_data()

    def run(self):
        """
        This method provides the data after being preprocessed
        """
        self.__pre_run()
        if len(self.adapters):
            self.__adapters()


