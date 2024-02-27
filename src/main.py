#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This module runs the main class

#####################
#   Native Imports  #
#####################
import sys
import traceback
import argparse


######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from monitoring.mvc.controllers.prepare_experiment import ExperimentDesign
from utils import DMAConstants
from utils.DMALogger import logging

################
#   CONSTANTS  #
################
DEBUG = True

class Main():
    def __init__(self, sorting_type) -> None:
        self.sorting_type = sorting_type

    def get_parser(self):
        """
        Initiate the argparser
        """
        parser = argparse.ArgumentParser(
                    description='This class is responsible on launching an experiment using CAIS-DMA',
                    epilog='All Copyrights Reserved - drimawi@unibz.it')
        return parser

    def add_args(self, parser):
        """
        Add comman line arguments for automation
        """
        parser.add_argument('-t', '--time-frame-size', dest='time_frame', default=5,
                            help='Time frame size to compute ACR')
        parser = parser.parse_args()
        return parser

    def main(self):
        """
        The main meeting
        """
        parser = self.get_parser()
        parser = self.add_args(parser=parser)
        global TIME_FRAME_SIZE
        DMAConstants.TIME_FRAME_SIZE = int(parser.time_frame)
        exp_des = ExperimentDesign(self.sorting_type)
        return exp_des.run()


try:
    exp_des = Main("normal")
    rc = exp_des.main()
    sys.exit(rc)
except Exception as exp:
    if not DEBUG:
        logging.error("Failed due to: {}".format(str(exp)))
        sys.exit(1)
    else:
        logging.error(traceback.format_exc())
        sys.exit(1)
