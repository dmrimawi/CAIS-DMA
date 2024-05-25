#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# Plotting the ACR

#####################
#   Native Imports  #
#####################
import os

######################
#   Modules Imports  #
######################
from matplotlib import pyplot as plt
import numpy as np

####################
#   Local Imports  #
####################
from utils import DMAConstants
from utils.DMACommon import Common
from utils.DMALogger import logging

################
#   CONSTANTS  #
################
REGION_START_INDX = 0
REGION_END_INDX = 1
REGION_COLOR_INDX = 2
REGION_NAME_INDX = 3
STEADY_STATE = 0
PERFORMANCE_DEGRADATION_STATE = 1
RECOVERING_STATE = 2
RECOVERED_STATE = 3
MECHANISM_SUPPORT = 4
STEADY_STATE_START_ACR = 1
PERFORMANCE_DEGRADATION_STATE_ENDS_ACR = 0

class ACRPlot():
    def __init__(self, csv_file, time_frame_size, satisfactory_value = 0.5) -> None:
        self.csv_file = csv_file
        self.time_frame_size = time_frame_size
        self.plot_thread = None
        self.plot_figure = None
        # white_gray = '#F4F3F3'
        # light_gray = '#D3D3D3'
        # medium_gray = '#A9A9A9'
        # dark_gray = '#696969'
        # charcoal_gray = '#555555'
        color_code_1 = "#00FF00"  # Green
        color_code_2 = "#FF0000"  # Red
        color_code_3 = "#0000FF"  # Blue
        color_code_4 = "#FFFF00"  # Yellow
        color_code_5 = "#FF00FF"  # Magenta
        self.regions = [
           [0, 0, color_code_1, 'Steady State'],
           [0, 0, color_code_2, 'Performance Degradation State'],
           [0, 0, color_code_3, 'Recovering State'],
           [0, 0, color_code_4, 'Recovered State'],
           [0, 0, color_code_5, 'Mechanism Support']]
        self.satisfactory_value = satisfactory_value

    def __get_x_y(self):
        y_data = Common.load_files_pandas(self.csv_file)[DMAConstants.CSV_ACR_DUMP_FIELD_NAME]
        x_data = range(1, len(y_data) + 1)
        return x_data, y_data

    def __compute_threshold(self, y, disrupt):
        threshold = 0
        if len(y) > disrupt:
            threshold = min(y[self.regions[STEADY_STATE][REGION_START_INDX]:self.regions[STEADY_STATE][REGION_END_INDX]])
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

    def define_regions(self, acr_values, threshold):
        current_state = -1
        iteration = 1
        potential_degradation = -1
        mechanism_support_start = -1
        mechanism_support_end = -1
        length_of_steady = 0
        recovered_flag = 0
        for acr in acr_values:
            if current_state == -1 and acr == STEADY_STATE_START_ACR:
                current_state = 0
                self.regions[STEADY_STATE][REGION_START_INDX] = iteration
            if current_state == 0:
                length_of_steady = length_of_steady + 1
                self.regions[STEADY_STATE][REGION_END_INDX] = iteration
            if current_state == 0 and potential_degradation == -1 and acr <= self.satisfactory_value:
                potential_degradation = iteration
            if current_state == 0 and potential_degradation != -1 and acr > self.satisfactory_value:
                potential_degradation = -1
            if current_state == 0 and potential_degradation != -1 and acr <= PERFORMANCE_DEGRADATION_STATE_ENDS_ACR:
                i = iteration
                acr_under_performance = acr_values[i - 1]
                while True:
                    i = i - 1
                    if acr_values[i - 1] > acr_under_performance:
                        acr_under_performance = acr_values[i - 1]
                    else:
                        potential_degradation = i + 1
                        break
                if potential_degradation > self.regions[STEADY_STATE][REGION_START_INDX]:
                    length_of_steady = self.regions[STEADY_STATE][REGION_END_INDX] - \
                        self.regions[STEADY_STATE][REGION_START_INDX]
                    self.regions[STEADY_STATE][REGION_END_INDX] = potential_degradation
                    self.regions[PERFORMANCE_DEGRADATION_STATE][REGION_START_INDX] = potential_degradation
                    self.regions[PERFORMANCE_DEGRADATION_STATE][REGION_END_INDX] = iteration
                    self.regions[RECOVERING_STATE][REGION_START_INDX] = iteration
                    current_state = 2
                else:
                    self.regions[STEADY_STATE][REGION_START_INDX] = 0
                    self.regions[STEADY_STATE][REGION_END_INDX] = 0
                    current_state = -1
            if DMAConstants.SELECTED_MECHANISM.lower() != DMAConstants.INTERNAL_MECHANISM.lower() and current_state > 0:
                need_mechanism = bool(Common.load_files_pandas(self.csv_file).iloc[iteration-1]['NeedMechanism'])
                if need_mechanism:
                    recovered_flag = 0
                    if mechanism_support_start == -1:
                        mechanism_support_start = iteration
                    else:
                        mechanism_support_end = iteration
                        self.regions[MECHANISM_SUPPORT][REGION_START_INDX] = mechanism_support_start
                        self.regions[MECHANISM_SUPPORT][REGION_END_INDX] = mechanism_support_end
            if current_state == 2:
                self.regions[RECOVERING_STATE][REGION_END_INDX] = iteration
                if acr <  threshold:
                    recovered_flag = 0
                else:
                    recovered_flag = recovered_flag + 1
                if recovered_flag == length_of_steady:
                    self.regions[RECOVERING_STATE][REGION_END_INDX] = iteration - recovered_flag + 1
                    self.regions[RECOVERED_STATE][REGION_START_INDX] = iteration - recovered_flag + 1
                    self.regions[RECOVERED_STATE][REGION_END_INDX] = iteration
                    if DMAConstants.FIX_AFTER_RECOVERED:
                        global STEADY_DISRUPTED_FIXED_ITERATIONS
                        new_length = iteration - DMAConstants.STEADY_DISRUPTED_FIXED_ITERATIONS[0]
                        DMAConstants.STEADY_DISRUPTED_FIXED_ITERATIONS = (DMAConstants.STEADY_DISRUPTED_FIXED_ITERATIONS[0], \
                                                                          new_length, new_length)
                        logging.info("System Has Recovered, changing the duration of the disruptive state")
                        logging.info(iteration - DMAConstants.STEADY_DISRUPTED_FIXED_ITERATIONS[0] + 1)
                    break
            iteration = iteration + 1

    def draw_regions(self):
        for region in self.regions:
            if "Mechanism" in region[REGION_NAME_INDX]:
                plt.axvspan(region[REGION_START_INDX], region[REGION_END_INDX], ymin=0.01, ymax=0.99, alpha=0.5, \
                            color=region[REGION_COLOR_INDX])
            else:
                plt.axvspan(region[REGION_START_INDX], region[REGION_END_INDX], ymin=-0.01, ymax=1.01, alpha=0.5, \
                            color=region[REGION_COLOR_INDX])
        # Create a custom legend for regions
        legend_labels = [region[REGION_NAME_INDX] for region in self.regions]
        legend_colors = [region[REGION_COLOR_INDX] for region in self.regions]
        legend_patches = [plt.Rectangle((0, 0), 1, 1, fc=color) for color in legend_colors]  # Create colored squares for legend
        plt.legend(legend_patches, legend_labels, loc='lower right', facecolor='none', shadow=False, fancybox=False, 
                bbox_to_anchor=(1, 0), frameon=True, edgecolor='black', 
                labelcolor='black', handlelength=2, handleheight=2, handletextpad=1)

    def draw_graph(self, disrupt, fix, threshold=0, fill=(0, 0), trending_line=1):
        if self.plot_figure is not None:
            plt.close(self.plot_figure)
            self.plot_figure = None
        self.plot_figure = plt.figure()
        self.plot_figure.set_size_inches(13, 6)
        plt.rcParams["font.family"] = "Times New Roman"
        x_data, y_data = self.__get_x_y()
        if threshold == 0:
            threshold = self.__compute_threshold(y_data, disrupt)
        plt.xlabel("Time Frames of Size {}".format(self.time_frame_size))
        plt.ylabel("Autonomous Classification Ratio (ACR)")
        plt.scatter(x_data, y_data, s=0.5, color='black')
        if trending_line > 1:
            trending_line = self.calculate_trending_line(x_data, y_data, trending_line)
            plt.plot(x_data, trending_line, linewidth=0.5, color='black')
        else:
            plt.plot(x_data, y_data, linewidth=0.5, color='black')
        plt.xticks(np.arange(0, max(x_data)+20, 20))
        if disrupt < len(x_data):
            plt.axvline(x=disrupt, color='k', label='Turn off the lights')
        if fix < len(x_data):
            plt.axvline(x=fix, color='k', label='Turn the lights back on')
        if threshold > 0:
            plt.axhline(y=threshold, color='k', alpha=0.5, label='ACR Threshold')
        # Fill backgroun
        if fill[0] != 0 or fill[1] != 0:
            plt.axvspan(fill[0], fill[1], alpha=0.15, color='silver')
        plt.grid(True)
        self.define_regions(y_data, threshold)
        self.draw_regions()
        if DMAConstants.SHOW_PLOT_DIAGRAM:
            plt.draw()
            plt.pause(.5)
        plt.savefig(os.path.join(os.path.dirname(self.csv_file), DMAConstants.ACR_DIAGRAM_FILENAME), format='pdf')


