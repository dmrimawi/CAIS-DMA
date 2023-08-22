#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This command line script aims to prepare the confs.ini file, the preperation can be from scratch
# or by saving old confs
# Note that this is a stand alone script, and not part of the framework. Thus, the local imports
# are from the current directory since it is expected to run from its directory.

#####################
#   Native Imports  #
#####################
import sys
import os
import configparser
import argparse

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
import DMAConstants
from DMALogger import logging

################
#   CONSTANTS  #
################


class ConfsGen:

    def __init__(self):
        """
        Class constructor
        """
        pass

    def get_parser(self):
        """
        Initiate the argparser
        """
        parser = argparse.ArgumentParser(
                    description='Generates/Updates the configuration file confs.ini',
                    epilog='All Copyrights Reserved - drimawi@unibz.it')
        return parser

    def add_args(self, parser):
        """
        Add comman line arguments for automation
        """
        # The ini filename to read/write the confs
        general_options = parser.add_argument_group('General Options')
        general_options.add_argument('-f', '--ini-file', default="confs.ini", dest='ini_file',
                            help='The ini file name, to store/read the confs')
        # Instead of prompting the user to insert new confs values, use the one already exists in ini_file
        general_options.add_argument('--use-old-confs', default=False, dest='old_confs', action='store_true',
                            help='Do not prompt the user for custom confs and use the ini file data \
                                Note: This is only available in case of the existance of old confs')
        # The dataset folder used to test the CAIS-DMA
        data_options = parser.add_argument_group('Data Related Options')
        data_options.add_argument('--dataset', dest='dataset', default='color_classification',
                            help='Dataset folder name')
        # Preprocessing configs
        data_options.add_argument('-p', '--preprocessors', nargs='*', dest='preprocessors', default=[],
                            help='Preprocessors python files names list (in order)')
        data_options.add_argument('-d', '--disruptors', nargs='*', dest='disruptors', default=[],
                            help='Disruptors python files names list (in order)')
        data_options.add_argument('-s', '--data-split', dest='data_split', default=33,
                            help='The percentage to split the data before running the distributers')
        data_options.add_argument('--select-data-randomly', dest='data_random_selection', default=False,
                            action='store_true', help='Feeding the data to the system randomly')
        # Decision making configs
        decision_making_options = parser.add_argument_group('Decision Making Options')
        decision_making_options.add_argument('-a', '--actions', nargs='*', dest='actions', default=[],
                            help='List of actions to consider during decsion making process')
        decision_making_options.add_argument('-m', '--machanisms', nargs='*', dest='mechanisms', default=[],
                            help='List of mechanisms to consider during decsion making process')
        decision_making_options.add_argument('--performance-measurement', dest='per_measurement', default='ACR',
                            help='Set the performance measurement class')
        # Results configs
        results_options = parser.add_argument_group('Results Options')
        results_options.add_argument('--dump', dest='dump', default='dump', 
                                     help='Set the dump directory')
        return parser

    def check_paths_exits(self, root, dirs):
        """
        This methods loops over the given os.path.join(root, dirs**) and return non-existance directories
        """
        not_exit = []
        for dir in dirs:
            if not os.path.exists(os.path.join(root, dir)):
                not_exit.append(os.path.exists(os.path.join(root, dir)))
        return not_exit

    def verify_args(self, parser):
        """
        This method verify that all arguements are inserted correctly
        """
        rc = DMAConstants.SUCCESS
        config = configparser.ConfigParser()
        errors = []
        parser = parser.parse_args()
        if not os.path.isfile(parser.ini_file):
            errors.append("File: {} does not exist, or not a file.".format(parser.ini_file))
            rc = rc or DMAConstants.FAIL
        else:
            config.read(parser.ini_file)
        if (not config.sections() or any(sec not in config.sections() for sec in DMAConstants.LEVEL_1_SECTIONS)) \
            and parser.old_confs:
            errors.append("Cannot use old confs, while ini file is empty or corrupted")
            rc = rc or DMAConstants.FAIL
        # Data options verification
        if not os.path.exists(os.path.join(DMAConstants.DATASET, parser.dataset)):
            errors.append("No such file or direcotory exists for dataset: {}".format(os.path.join( \
                                                            DMAConstants.DATASET, parser.dataset)))
            rc = rc or DMAConstants.FAIL
        preprocessors_not_exist = self.check_paths_exits(DMAConstants.PREPROCESSORS, parser.preprocessors)
        if preprocessors_not_exist:
            errors.append("The following preprocessors does not exists: {}".format("\n".join(preprocessors_not_exist)))
            rc = rc or DMAConstants.FAIL
        disruptors_not_exist = self.check_paths_exits(DMAConstants.DISRUPTORS, parser.disruptors)
        if disruptors_not_exist:
            errors.append("The following preprocessors does not exists: {}".format("\n".join(disruptors_not_exist)))
            rc = rc or DMAConstants.FAIL
        try:
            x = float(parser.data_split)
        except Exception as exp:
            errors.append("Failed to parse the data split rate: {}, exception: {}".format(parser.data_split), str(exp))
            rc = rc or DMAConstants.FAIL
        # Decision making options verification
        actions_not_exist = self.check_paths_exits(DMAConstants.ACTIONS, parser.actions)
        if actions_not_exist:
            errors.append("The following actions does not exists: {}".format("\n".join(actions_not_exist)))
            rc = rc or DMAConstants.FAIL
        mechanisms_not_exist = self.check_paths_exits(DMAConstants.MECHANISMS, parser.mechanisms)
        if mechanisms_not_exist:
            errors.append("The following mechanisms does not exists: {}".format("\n".join(mechanisms_not_exist)))
            rc = rc or DMAConstants.FAIL
        if not os.path.exists(os.path.join(DMAConstants.PERFORMANCE_MEASUREMENTS, parser.per_measurement)):
            errors.append("The following performance measure does not exists: {}".format(os.path.join( \
                                                    DMAConstants.PERFORMANCE_MEASUREMENTS,  parser.per_measurement)))
            rc = rc or DMAConstants.FAIL
        # Results options verification
        if not os.path.exists(os.path.join(DMAConstants.RESULTS, parser.dump)):
            errors.append("The following dump folder does not exists: {}".format(os.path.join(DMAConstants.RESULTS, \
                                                                                              parser.dump)))
            rc = rc or DMAConstants.FAIL
        if rc:
            logging.error("Error(s) during parsing the command arguments: {}".format("\n".join(errors)))
            parser.print_help()
        return rc, parser

    def parse_cmd_line(self):
        """
        This method returns the status of reading command line options
        and the parsed attributes
        """
        parser = self.get_parser()
        parser = self.add_args(parser)
        rc, parser = self.verify_args(parser)
        return rc, parser

    def prepare_default_section(self, parser, config):
        """
        This method prepares the default section
        """
        default_sec = {}
        default_sec['home.path'] = DMAConstants.HOME
        default_sec['src.path'] = DMAConstants.SRC
        config[DMAConstants.DEFAULT_SEC] = default_sec
        return config

    def prepare_data_section(self, parser, config):
        """
        This method prepares the data section
        """
        data_sec = {}
        if parser.old_confs and DMAConstants.DATA_SEC in config:
            data_sec = config[DMAConstants.DATA_SEC]
        else:
            data_sec[DMAConstants.DATA_DATASET_PATH_INI] = os.path.join(DMAConstants.DATASET, parser.dataset)
            data_sec[DMAConstants.PREPROCESSORS_LIST_INI] = parser.preprocessors
            data_sec[DMAConstants.DISRUPTORS_LIST_INI] = parser.disruptors
            data_sec[DMAConstants.SPLIT_DATA_VALUE_INI] = parser.data_split
            data_sec[DMAConstants.DATASET_FEED_RANDOM_INI] = parser.data_random_selection
        data_sec[DMAConstants.DATA_PATH_INI] = DMAConstants.DATA
        data_sec[DMAConstants.DATA_ALL_DATASETS_PATH_INI] = DMAConstants.DATASET
        data_sec[DMAConstants.DATA_PREPROCESSING_PATH_INI] = DMAConstants.PREPROCESSING
        data_sec[DMAConstants.DATA_PREPROCESSORS_PATH_INI] = DMAConstants.PREPROCESSORS
        data_sec[DMAConstants.DATA_DISRUPTORS_PATH_INI] = DMAConstants.DISRUPTORS
        config[DMAConstants.DATA_SEC] = data_sec
        return config

    def prepare_decision_making_section(self, parser, config):
        """
        This method prepares the decision making section
        """
        decition_making_sec = {}
        if parser.old_confs and DMAConstants.DECISION_MAKING_SEC in config:
            decition_making_sec = config[DMAConstants.DECISION_MAKING_SEC]
        else:
            decition_making_sec['actuator.actions.list'] = parser.actions
            decition_making_sec['actuator.mechanisms.list'] = parser.mechanisms
            decition_making_sec['actuator.performance_measurements.pkj'] = parser.per_measurement
        decition_making_sec['actuator.path'] = DMAConstants.DECISION_MAKING
        decition_making_sec['actuator.actions.path'] = DMAConstants.ACTIONS
        decition_making_sec['actuator.mechanisms.path'] = DMAConstants.MECHANISMS
        decition_making_sec['actuator.performance_measurements.path'] = DMAConstants.PERFORMANCE_MEASUREMENTS
        config[DMAConstants.DECISION_MAKING_SEC] = decition_making_sec
        return config

    def prepare_results_section(self, parser, config):
        """
        This method prepares the results section
        """
        results_sec = {}
        if parser.old_confs and DMAConstants.RESULTS_SEC in config:
            results_sec = config[DMAConstants.RESULTS_SEC]
        else:
            results_sec['monitoring.dumps.path'] = os.path.join(DMAConstants.RESULTS, parser.dump)
        results_sec['monitoring.path'] = DMAConstants.DECISION_MAKING
        config[DMAConstants.RESULTS_SEC] = results_sec
        return config

    def write_inis_to_file(self, ini_file, config):
        """
        This method writes the confs to the ini_file
        """
        with open(ini_file, 'w') as configfile:
            config.write(configfile)

    def run(self):
        """
        This method runs the scrips steps
        """
        rc, parser = self.parse_cmd_line()
        if not rc:
            config = configparser.ConfigParser()
            config.read(parser.ini_file)
            config = self.prepare_default_section(parser, config)
            config = self.prepare_data_section(parser, config)
            config = self.prepare_decision_making_section(parser, config)
            config = self.prepare_results_section(parser, config)
            self.write_inis_to_file(parser.ini_file, config)
        return rc


try:
    congs_gen = ConfsGen()
    rc = congs_gen.run()
    sys.exit(rc)
except Exception as exp:
    logging.error("Failed due to: {}".format(str(exp)))
    sys.exit(1)
