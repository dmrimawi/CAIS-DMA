#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This module orchestrate applying preprocessors and disruptors 

#####################
#   Native Imports  #
#####################
import os
import math
import time
import random

######################
#   Modules Imports  #
######################
import zmq

####################
#   Local Imports  #
####################
from utils.DMALogger import logging
from utils.DMACommon import Common
from utils import DMAConstants
from utils.Exceptions.DMAException import DMAException
from simulator.preprocessing.disruptors.disruptors_factory import DisruptorsFactory
from simulator.preprocessing.adapters.adaptors_factory import AdaptorsFactory
from simulator.streamers.zmq.zmq_pub_sub import ZeroMQHandler
from actuator.action_selector import ActionSelector

################
#   CONSTANTS  #
################


class DataFeeder():
    def __init__(self, name: str, dataset_path: str, output_path: str, csv_file:str, \
                 split_rate: float, adapters=[], disruptors=[]):
        """
        Data Feeder Constructor
        """
        self.name = name
        self.desc = ''
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.csv_file = csv_file
        self.split_rate = split_rate
        self.adapters = adapters
        self.disruptors = disruptors
        self.data_frame = None

    def __apply(self, obj):
        """
        Call the disruptors methods
        """
        obj.fetch_dataset()
        obj.apply()
        obj.dump()

    def __disruptors(self):
        """
        This method responsible to apply the data changes from the selected disruptors
        """
        logging.info("Running disruptors: {}".format(self.disruptors))
        dis_factory = DisruptorsFactory(self.disruptors, self.name, self.desc, self.dataset_path, \
                                           self.output_path)
        while dis_factory.has_next():
            pre_obj = dis_factory.next()
            self.__apply(pre_obj)

    def __adapters(self):
        """
        This method responsible to convert data structure using the adapter
        """
        logging.info("Running Adapters: {}".format(self.adapters))
        adaptor_factory = AdaptorsFactory(self.adapters, self.name, self.desc, self.dataset_path, \
                                           self.output_path)
        while adaptor_factory.has_next():
            adapt_obj = adaptor_factory.next()
            self.__apply(adapt_obj)

    def __change_to_disrupted_per_group(self, groups, num):
        """
        This method loops over the groups and change the disrupted column from 0 to 1
        """
        for group in groups.indices.keys():
            num_to_change = num
            if num > len(groups.get_group(group)):
                num_to_change = len(groups.get_group(group))
            for index in groups.get_group(group).sample(n=num_to_change).index:
                self.data_frame.at[index, DMAConstants.DISRUPTED_COL_TITLE] = 1

    def __pick_data_to_disrupt(self):
        """
        This method creats a new column called disrupted (0, 1).
        In the dataframe, all raws with 1 value, will be selected to apply the disruptors on
        """
        if self.data_frame is not None:
            self.data_frame[DMAConstants.DISRUPTED_COL_TITLE] = 0
            length_of_data = len(self.data_frame)
            number_of_items_to_disrupt = math.floor(length_of_data * (self.split_rate / 100.0))
            groups = self.data_frame.groupby(DMAConstants.CSV_COL_CLASS_TITLE)
            number_of_groups = len(groups)
            number_of_items_to_disrupt_per_group = math.floor(number_of_items_to_disrupt / number_of_groups)
            self.__change_to_disrupted_per_group(groups, number_of_items_to_disrupt_per_group)
            Common.save_pandas_df_to_file(self.data_frame, os.path.join(self.output_path, self.csv_file))

    def __prepare_data(self):
        """
        This method perform preprocessing, and disruption over the data, and prepare it
        """
        if len(self.disruptors):
            self.__disruptors()

    def __pre_run(self):
        """
        Common pre running preperations
        """
        self.dataset_name = os.path.basename(self.dataset_path)
        workspace_path = os.path.join(self.output_path, self.dataset_name)
        Common.copy_directory(self.dataset_path, workspace_path)
        self.dataset_path = workspace_path
        self.output_path = workspace_path
        self.data_frame = Common.load_files_pandas(os.path.join(self.output_path, self.csv_file))
        self.__pick_data_to_disrupt()
        self.__prepare_data()

    def get_all_json_files_disrupted_normal(self):
        """
        This method returns a dictionarry with all files names
        seperated into two classes disrupted and normal
        """
        all_json_files = {'normal': {'Red': list(), 'Green': list(), 'Blue': list()}, \
                          'disrupted': {'Red': list(), 'Green': list(), 'Blue': list()}}
        for _, item in self.data_frame.iterrows():
            if item[DMAConstants.DISRUPTED_COL_TITLE] == 1:
                all_json_files['disrupted'][item[DMAConstants.CSV_COL_COLOR]].append(os.path.join(self.output_path, \
                                                    "{}.json".format(item[DMAConstants.FIELD_WITH_DATA_TITLE])))
            else:
                all_json_files['normal'][item[DMAConstants.CSV_COL_COLOR]].append(os.path.join(self.output_path, \
                                                    "{}.json".format(item[DMAConstants.FIELD_WITH_DATA_TITLE])))
        return all_json_files

    def new_object(self, json_file, zmq_handler, obj_publisher, teaching_publisher, classifier_subscriber, \
                   unclassifier_subscriber):
        """
        This method streams the new arriving object
        """
        time.sleep(1)
        if Common.check_if_file_dir_exists(json_file):
            received_data = None
            clf_recieved_data = None
            logging.info("Publishing the content of {}".format(json_file))
            data = Common.read_json_file(json_file)
            zmq_handler.publish_message(publisher_socket=obj_publisher, data=data)
            while True:
                try:
                    try:
                        clf_recieved_data = zmq_handler.receive_message(classifier_subscriber)
                        received_data = clf_recieved_data
                        break
                    except zmq.Again as e:
                        pass
                    received_data = zmq_handler.receive_message(unclassifier_subscriber)
                    break
                except zmq.Again as e:
                    pass
            logging.info("Classification for: {}".format(received_data))
            data[1]['Detections'][0]['Target'] = received_data['Target']
            selector = ActionSelector(self.name, self.desc, os.path.join(self.output_path, self.csv_file), data)
            data = selector.perform_action()
            if data["Teaching"]:
                zmq_handler.publish_message(publisher_socket=teaching_publisher, data=data)

    def normal_stream(self, seperated=(46, 82, 83)):
        """
        Streaming data in order
        """
        zmq_handler = ZeroMQHandler()
        obj_publisher = zmq_handler.create_publisher(address=DMAConstants.PUBLISH_ADDRESS, \
                                                     port=DMAConstants.PUBLISH_PORT)
        teaching_publisher = zmq_handler.create_publisher(address=DMAConstants.PUBLISH_ADDRESS, \
                                                          port=DMAConstants.TEACHING_PORT)
        classifier_subscriber = zmq_handler.create_subscriber(address=DMAConstants.SUBSCRIBE_ADDRESS, \
                                                              port=DMAConstants.SUBSCRIBE_PORT)
        unclassifier_subscriber = zmq_handler.create_subscriber(address=DMAConstants.SUBSCRIBE_ADDRESS, \
                                                                port=DMAConstants.SUBSCRIBE_UNCLS_PORT)
        choosen_objects = list()
        json_dataset_files = self.get_all_json_files_disrupted_normal()
        colors = ['Red', 'Green', 'Blue']
        counter = 1
        for i in range(0, len(seperated)):
            data_type_to_stream = ('normal', 'disrupted')[i % 2 != 0]
            for j in range(0, seperated[i]):
                color = colors[j % 3]
                logging.info(f"{counter}. Classifying a {data_type_to_stream} {color} Cube.")
                object_to_stream = random.choice(json_dataset_files[data_type_to_stream][color])
                while object_to_stream in choosen_objects:
                    object_to_stream = random.choice(json_dataset_files[data_type_to_stream][color])
                choosen_objects.append(object_to_stream)
                self.new_object(object_to_stream, zmq_handler, obj_publisher, teaching_publisher, classifier_subscriber, \
                                unclassifier_subscriber)
                counter = counter + 1
        obj_publisher.close()
        classifier_subscriber.close()
        teaching_publisher.close()
        unclassifier_subscriber.close()
        zmq_handler.terminate_context()

    def run(self):
        """
        This method provides the data after being preprocessed
        """
        self.__pre_run()
        if len(self.adapters):
            self.__adapters()
        else:
            raise DMAException("Missing adapters, Adapters are important to prepare data in the same structure \
                               expected by the CAIS under test.")
        self.normal_stream()
