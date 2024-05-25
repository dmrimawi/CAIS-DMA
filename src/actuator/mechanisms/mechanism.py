#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it

#####################
#   Native Imports  #
#####################


######################
#   Modules Imports  #
######################


####################
#   Local Imports  #
####################


################
#   CONSTANTS  #
################


class Mechanism:
    """
    This class definition defines a "Mechanism" class with a static method called "create_mechanism".
    """
    @staticmethod
    def create_mechanism(mechanism_type: str, actions_data, probabilities):
        """
        Create a mechanism based on the provided mechanism type, actions data, and probabilities.
        Parameters:
            mechanism_type (str): The type of mechanism to create.
            actions_data: The actions data for the mechanism.
            probabilities: The probabilities for the mechanism.
        Returns:
            GRGame or GROpt: An instance of GRGame or GROpt based on the mechanism type.
        
        Raises:
            ValueError: If the provided mechanism type is not 'grgame' or 'gropt'.
        """
        if mechanism_type.lower() == "grgame":
            from actuator.mechanisms.GResilience.GRGame import GRGame
            return GRGame(actions_data, probabilities)
        elif mechanism_type.lower() == "gropt":
            from actuator.mechanisms.GResilience.GROpt import GROpt
            return GROpt(actions_data, probabilities)
        else:
            raise ValueError("Invalid mechanism type. Supported types are 'grgame' and 'gropt'.")

