#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This python module contains the class responsible to create preprocessors

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
from simulator.preprocessing.factory import Factory

################
#   CONSTANTS  #
################
COLOR_CLASSIFICATION = "color_classification"
COLOR_CLASSIFICATION_DISRUPTORS = ["blur", "darkness"]


class DisruptorsFactory(Factory):
    def __init__(self, classes_list: list, name: str, desc: str, dataset_path: str, output_path: str):
        super().__init__(classes_list, name, desc, dataset_path, output_path)

    def __color_classification_disruptors_factory(self, class_name):
        """
        Factory method for the color classification dataset disruptors
        """
        obj = None
        if class_name in COLOR_CLASSIFICATION_DISRUPTORS:
            if class_name == "blur":
                from simulator.preprocessing.disruptors.color_classification.blur import Blur
                obj = Blur(self.name, self.desc, self.dataset_path, self.output_path)
            if class_name == "darkness":
                from simulator.preprocessing.disruptors.color_classification.darkness import Dark
                obj = Dark(self.name, self.desc, self.dataset_path, self.output_path)
        return obj

    def classes_factory(self, class_name):
        """
        Override the class_factory method in the abstract class Factory
        """
        # It is recommended to create a factory method per each dataset
        # The following calls the facotry method of color classification dataset
        base_dataset = os.path.basename(self.dataset_path)
        if base_dataset == COLOR_CLASSIFICATION:
            return self.__color_classification_disruptors_factory(class_name)
        return None
