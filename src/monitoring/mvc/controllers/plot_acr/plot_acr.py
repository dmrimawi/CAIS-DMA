#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# Plotting the ACR

#####################
#   Native Imports  #
#####################
import os
import threading


######################
#   Modules Imports  #
######################
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
# from labellines import labelLines

####################
#   Local Imports  #
####################
from utils import DMAConstants
from utils.DMACommon import Common
from utils.DMALogger import logging

################
#   CONSTANTS  #
################

class ACRPlot():
    def __init__(self, csv_file, time_frame_size) -> None:
        self.csv_file = csv_file
        self.time_frame_size = time_frame_size
        self.plot_thread = None
        self.plot_figure = None

    def __get_x_y(self):
        y_data = Common.load_files_pandas(self.csv_file)[DMAConstants.CSV_ACR_DUMP_FIELD_NAME]
        # Label the chart and set style
        x_data = range(1, len(y_data) + 1)
        return x_data, y_data

    def __compute_threshold(self, y, disrupt):
        threshold = 0
        if len(y) > disrupt:
            count = 0
            steady = False
            for acr in y:
                if steady and count < disrupt:
                    if threshold > acr:
                        threshold = acr
                elif not steady and acr == 1:
                    steady = True
                    threshold = 1
                count = count + 1
        return threshold

    def calculate_trending_line(self, x_data, y_data, window_size):
        trending_line = []
        for i in range(len(x_data)):
            if i < window_size // 2:
                trend = np.mean(y_data[:window_size])
            elif i >= len(x_data) - window_size // 2:
                trend = np.mean(y_data[-window_size:])
            else:
                trend = np.mean(y_data[i - window_size // 2: i + window_size // 2])
            trending_line.append(trend)
        return trending_line

    def draw_graph(self, disrupt, fix, threshold=0, fill=(0, 0), trending_line=1):
        if self.plot_figure is not None:
            plt.close(self.plot_figure)
            self.plot_figure = None
        self.plot_figure = plt.figure()
        plt.rcParams["font.family"] = "Times New Roman"
        x_data, y_data = self.__get_x_y()
        if threshold == 0:
            threshold = self.__compute_threshold(y_data, disrupt)
        plt.xlabel("Time Frames of Size {}".format(self.time_frame_size))
        plt.ylabel("Autonomous Classification Ratio (ACR)")
        # Plot the scatter chart
        plt.scatter(x_data, y_data, s=0.5, color='black')
        if trending_line > 1:
            trending_line = self.calculate_trending_line(x_data, y_data, trending_line)
            plt.plot(x_data, trending_line, linewidth=0.5, color='black')
        else:
            plt.plot(x_data, y_data, linewidth=0.5, color='black')
        plt.xticks(np.arange(0, max(x_data)+10, 10))

        # Plot lines
        # if steady < len(x_data):
        #     plt.axvline(x=steady, color='k', label='Start of steady State')
        if disrupt < len(x_data):
            plt.axvline(x=disrupt, color='k', label='Turn off the lights')
        if fix < len(x_data):
            plt.axvline(x=fix, color='k', label='Turn the lights back on')
        if threshold > 0:
            plt.axhline(y=threshold, color='k', alpha=0.5, label='ACR Threshold')
        # Fill backgroun
        if fill[0] != 0 or fill[1] != 0:
            plt.axvspan(fill[0], fill[1], alpha=0.15, color='silver')

        # Change the default save directory
        # plt.rcParams["savefig.directory"] = os.chdir(os.path.dirname(__file__))

        # Show the chart
        # labelLines(plt.gca().get_lines(), xvals=(max(x_data)-30, max(x_data)), zorder=2.5, align=True, backgroundcolor="none")
        plt.grid(True)
        plt.draw()
        plt.pause(.5)
        plt.savefig(os.path.join(os.path.dirname(self.csv_file), DMAConstants.ACR_DIAGRAM_FILENAME), format='pdf')


