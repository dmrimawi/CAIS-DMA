#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This is the loging class to print command line messages

class logging():
    def __init__(self):
        pass

    def info(self, msg):
        # TODO: in addition to print write to log file
        print("-I- {}".format(msg))
    
    def warning(self, msg):
        # TODO: in addition to print write to log file
        print("-W- {}".format(msg))
    
    def error(self, msg):
        # TODO: in addition to print write to log file
        print("-E- {}".format(msg))

    def debug(self, msg):
        # TODO: writes to log files only
        pass
