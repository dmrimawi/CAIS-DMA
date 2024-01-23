#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This class converts the provided image to a JSON structure
# As CORAL classifier takes the data

#####################
#   Native Imports  #
#####################
import os
import json
import base64
import time


######################
#   Modules Imports  #
######################
import cv2 as cv
import numpy as np


####################
#   Local Imports  #
####################
from utils.Exceptions.DMAException import DMAException
from utils.DMACommon import Common
from utils import DMAConstants
from simulator.preprocessing.adapters.adapter import Adapter

################
#   CONSTANTS  #
################


class ColorClassificationAdapter(Adapter):
    def __init__(self, name: str, desc: str, dataset_path: str, output_path: str) -> None:
        """
        This Adaptor convert the object passed (image) to a JSON format as the MLClassifier expects
        """
        if desc == '' or desc is None:
            self.desc = """
                            This Adaptor convert the objects (images)
                            to a JSON format as the MLClassifier expects
                        """
        super().__init__(name, desc, dataset_path, output_path)

    def get_json_example(self):
        """
        This method creates an empty dictionary of CORAL JSON format
        """
        example_path = os.path.join(self.dataset_path, "{}.json".format(DMAConstants.ADAPTER_EXAMPLE_FILE_NAME))
        json_example = None
        if os.path.exists(example_path):
            with open(example_path) as f:
                json_example = json.load(f)
        else:
            raise DMAException("The example path doesn't exist: {}".format(example_path))           
        return json_example

    def encode_image_to_base64(self, image):
        """
        Encode a NumPy image array to base64 string.

        Parameters:
        - image (numpy.ndarray): The image represented as a NumPy array.

        Returns:
        - str: The base64-encoded image string.
        """
        _, img_encoded = cv.imencode('.png', image)
        return base64.b64encode(img_encoded).decode('utf-8')

    def fetch_dataset(self):
        # Create a list of all images in the dataset
        data_frame = Common.load_files_pandas(os.path.join(self.dataset_path, DMAConstants.CSV_FILE_NAME))
        self.all_dataset_imgs = list()
        for _, data in data_frame.iterrows():
            self.all_dataset_imgs.append(os.path.join(self.dataset_path, data[DMAConstants.FIELD_WITH_DATA_TITLE]))

    def apply(self):
        self.imgs_data = {}
        obj_id = 1   
        for img_f in self.all_dataset_imgs:
            f_name = os.path.basename(img_f)
            image = cv.imread(img_f)
            image = cv.resize(image, (51, 48))
            encoded_image = self.encode_image_to_base64(image)
            self.imgs_data[f_name] = self.get_json_example()
            self.imgs_data[f_name][1]['Detections'][0]['Data'] = encoded_image
            current_time = time.time() + 10
            self.imgs_data[f_name][0]['AcquisitionTime'] = current_time
            self.imgs_data[f_name][1]['AcquisitionTime'] = current_time
            self.imgs_data[f_name][1]['DetectionTime'] = current_time + 13
            self.imgs_data[f_name][1]['Detections'][0]['ObjectID'] = obj_id
            obj_id = obj_id + 1
            
    
    def dump(self):
        for name, data in self.imgs_data.items():
            with open(os.path.join(self.output_path, "{}.json".format(name)), "w") as file:
                json.dump(data, file)
