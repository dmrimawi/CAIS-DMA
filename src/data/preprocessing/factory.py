#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This abstract module is to create the necessary modules to create a objects factory class

#####################
#   Native Imports  #
#####################
from abc import ABC, abstractmethod 

######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################


################
#   CONSTANTS  #
################


class Factory(ABC):
    @abstractmethod
    def __init__(self, classes_list: list, name: str, desc: str, dataset_path: str, output_path: str):
        self.classes_list = classes_list
        self.name = name
        self.desc = desc
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.counter = 0

    @abstractmethod
    def classes_factory(self, class_name):
        """
        Override this method for the specific dataset preprocessors/disruptors factory method
        Prefered not be called by outside the class, and should use has_next and next methods
        """
        pass

    def has_next(self):
        """
        Check if all classes where passed over in the @classes_list
        """
        return self.counter < len(self.classes_list)
    
    def next(self):
        """
        Return the next class instance
        """
        obj = None
        if self.has_next():
            obj = self.classes_factory(class_name=self.classes_list[self.counter])
            self.counter = self.counter + 1
        return obj
