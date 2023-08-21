#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This module runs the main class

#####################
#   Native Imports  #
#####################
import sys

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from results.mvc.controllers.prepare_experiment import ExperimentDesign
from src.utils.DMALogger import logging

################
#   CONSTANTS  #
################


class Main():
    def __init__(self, sorting_type) -> None:
        self.sorting_type = sorting_type

    def main(self):
        """
        The main meeting
        """
        exp_des = ExperimentDesign(self.sorting_type)
        return exp_des.run()


try:
    exp_des = Main("normal")
    rc = exp_des.main()
    sys.exit(rc)
except Exception as exp:
    logging.error("Failed due to: {}".format(str(exp)))
    sys.exit(1)
