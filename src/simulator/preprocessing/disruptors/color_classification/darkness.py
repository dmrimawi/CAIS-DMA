#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This is a Disruptor class that takes a dataset of images and blur them

#####################
#   Native Imports  #
#####################
import os

######################
#   Modules Imports  #
######################
import cv2 as cv

####################
#   Local Imports  #
####################
from simulator.preprocessing.disruptors.disruptors import Disruptor
from utils.Exceptions.DMAException import DMAException
from utils.DMACommon import Common
from utils import DMAConstants

################
#   CONSTANTS  #
################


class Dark(Disruptor):
    def __init__(self, name: str, desc: str, dataset_path: str, output_path: str, value=-50) -> None:
        """
        This Disruptor apply darkness and brightness changes to an images with a specific value
        """
        self.value = value
        if desc == '' or desc is None:
            self.desc = """
                            This Disruptor is darkening the images to a specific value = {}
                            It reads images and dumps images as well
                        """.format(self.value)
        super().__init__(name, desc, dataset_path, output_path)
    
    def fetch_dataset(self):
        # Create a list of all images in the dataset
        data_frame = Common.load_files_pandas(os.path.join(self.dataset_path, DMAConstants.CSV_FILE_NAME))
        disrupted_data = data_frame.loc[data_frame[DMAConstants.DISRUPTED_COL_TITLE] == 1]
        self.all_dataset_imgs = list()
        for _, data in disrupted_data.iterrows():
            self.all_dataset_imgs.append(os.path.join(self.dataset_path, data[DMAConstants.FIELD_WITH_DATA_TITLE]))

    def change_brightness(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)
        v = cv.add(v, self.value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv.merge((h, s, v))
        return cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)

    def apply(self):
        self.imgs_data = {}
        for img_f in self.all_dataset_imgs:
            img = cv.imread(img_f)
            dark = self.change_brightness(img)
            f_name = os.path.basename(img_f)
            self.imgs_data[f_name] = dark
    
    def dump(self):
        for name, data in self.imgs_data.items():
            cv.imwrite(os.path.join(self.output_path, name), data)

