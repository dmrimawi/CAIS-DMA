#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This is the loging class to print command line messages

class logging():
    def __init__(self):
        pass

    @staticmethod
    def info(msg):
        # TODO: in addition to print write to log file
        print("-I- {}".format(msg))

    @staticmethod
    def warning(msg):
        # TODO: in addition to print write to log file
        print("-W- {}".format(msg))

    @staticmethod
    def error(msg):
        # TODO: in addition to print write to log file
        print("-E- {}".format(msg))

    @staticmethod
    def debug(msg):
        # TODO: writes to log files only
        pass
