#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This python module aims to generate the command line to execute a full experiment

#####################
#   Native Imports  #
#####################
import os
import configparser

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from utils import DMAConstants
from simulator.data_feeder import DataFeeder

################
#   CONSTANTS  #
################
NORMAL_SORT = "normal"
LABEL_SORT = "label"
MIX_SORT = "mix"
RANDOM_SORT = "random"


class ExperimentDesign():
    def __init__(self, sorting_type) -> None:
        """
        ExperimentDesin Constructor
        Sorting_types can be one of: [normal, label_sort, mix, random]
        normal: read the data as they are
        label: read the data sorted (each class at a time)
        mix: read the data one item from each class at a time
        random: read data randomly
        """
        self.sorting_type = sorting_type

    def get_dataset_path(self, configs):
        """
        Returns the dataset path as in the ini file
        """
        return configs[DMAConstants.DATA_SEC][DMAConstants.DATA_DATASET_PATH_INI]

    def get_experiment_id_dir(self, configs):
        """
        Create the name of the experiment, and its directory
        """
        dumps_dir = configs[DMAConstants.RESULTS_SEC][DMAConstants.RESULTS_DUMPS_PATH_INI]
        if not os.path.exists(dumps_dir):
            os.mkdir(dumps_dir)
        dataset_name = os.path.basename(self.get_dataset_path(configs))
        experiments_root = os.path.join(dumps_dir, dataset_name)
        if not os.path.exists(experiments_root):
            os.mkdir(experiments_root)
        new_experiment = 1
        all_expers = os.listdir(experiments_root)
        if len(all_expers) > 0:
            all_expers.sort(key=int)
            new_experiment = int(all_expers[-1]) + 1
        new_experiment_dir = os.path.join(experiments_root, str(new_experiment))
        os.mkdir(new_experiment_dir)
        return new_experiment, new_experiment_dir

    def get_the_split_rate(self, configs):
        """
        This method extracts the split rate from the configs file
        """
        return float(configs[DMAConstants.DATA_SEC][DMAConstants.SPLIT_DATA_VALUE_INI])

    def get_adapters_list(self, configs):
        """
        This method extracts the preorpcessors list from the configs file
        """
        return eval(configs[DMAConstants.DATA_SEC][DMAConstants.ADAPTERS_LIST_INI])

    def get_disruptors_list(self, configs):
        """
        This method extracts the disruptors list from the configs file
        """
        return eval(configs[DMAConstants.DATA_SEC][DMAConstants.DISRUPTORS_LIST_INI])

    def run(self):
        """
        This memthod runs the experiment
        Sorting_types can be one of: [normal, label_sort, mix, random]
        normal: read the data as they are
        label_sort: read the data sorted (each class at a time)
        mix: read the data one item from each class at a time
        random: read data randomly
        """
        config = configparser.ConfigParser()
        config.read(DMAConstants.INI_FILE_PATH)
        dataset = self.get_dataset_path(config)
        name, output_dir = self.get_experiment_id_dir(config)
        csv_file = DMAConstants.CSV_FILE_NAME
        split_rate = self.get_the_split_rate(config)
        adapters = self.get_adapters_list(config)
        disruptors = self.get_disruptors_list(config)
        if self.sorting_type == NORMAL_SORT:
            data_feeder = DataFeeder(name, dataset, output_dir, csv_file, split_rate, \
                                     adapters=adapters, disruptors=disruptors)
            data_feeder.run()
        return 0

