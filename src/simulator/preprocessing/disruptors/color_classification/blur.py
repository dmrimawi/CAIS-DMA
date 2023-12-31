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


class Blur(Disruptor):
    def __init__(self, name: str, desc: str, dataset_path: str, output_path: str, ratio=(5, 5)) -> None:
        """
        This Disruptor blur images to a specific ratio, where ratio in [0, 1]
        """
        if not type(ratio) == tuple:
            raise DMAException("In Disruptor {}, ratio value {}, while it should be tuple of two integers".format(
                self.name, ratio
            ))
        self.ratio = ratio
        if desc == '' or desc is None:
            self.desc = """
                            This Disruptor is blur the images to a specific ratio = {}
                            It reads images and dumps images as well
                        """.format(self.ratio)
        super().__init__(name, desc, dataset_path, output_path)
    
    def fetch_dataset(self):
        # Create a list of all images in the dataset
        data_frame = Common.load_files_pandas(os.path.join(self.dataset_path, DMAConstants.CSV_FILE_NAME))
        disrupted_data = data_frame.loc[data_frame[DMAConstants.DISRUPTED_COL_TITLE] == 1]
        self.all_dataset_imgs = list()
        for _, data in disrupted_data.iterrows():
            self.all_dataset_imgs.append(os.path.join(self.dataset_path, data[DMAConstants.FIELD_WITH_DATA_TITLE]))

    def apply(self):
        self.imgs_data = {}
        for img_f in self.all_dataset_imgs:
            img = cv.imread(img_f)
            blur = cv.blur(img, self.ratio)
            f_name = os.path.basename(img_f)
            self.imgs_data[f_name] = blur
    
    def dump(self):
        for name, data in self.imgs_data.items():
            cv.imwrite(os.path.join(self.output_path, name), data)

