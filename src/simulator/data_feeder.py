#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This module orchestrate applying preprocessors and disruptors 

#####################
#   Native Imports  #
#####################
import os

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################
from simulator.preprocessing.disruptors.disruptors_factory import DisruptorsFactory
from utils.DMALogger import logging
from utils.DMACommon import Common

################
#   CONSTANTS  #
################


class DataFeeder():
    def __init__(self, name: str, dataset_path: str, output_path: str, \
                 split_rate, adapters=[], disruptors=[]):
        """
        Data Feeder Constructor
        """
        self.name = name
        self.desc = ''
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.split_rate = split_rate
        self.adapters = adapters
        self.disruptors = disruptors

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
        self.__prepare_data()

    def run(self):
        """
        This method provides the data after being preprocessed
        """
        self.__pre_run()
        if len(self.adapters):
            self.__adapters()


