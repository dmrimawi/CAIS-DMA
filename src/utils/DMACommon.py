#!/usr/bin/env python3

#       Class Desciption
# Author: Diaeddin Rimawi
# Email: dmrimawi@gmail.com + drimawi@unibz.it
# This module contains common static methods

#####################
#   Native Imports  #
#####################
import os
import shutil
import json
import csv

######################
#   Modules Imports  #
######################
import pandas as pd

####################
#   Local Imports  #
####################
from utils.Exceptions.DMAException import DMAException

################
#   CONSTANTS  #
################


class Common():
    def __ini__(self):
        pass

    @staticmethod
    def check_if_file_dir_exists(file_dir_path, is_file=False):
        """
        Checks if file or directory exists
        """
        return (is_file and os.path.isfile(file_dir_path)) or \
           (not is_file and os.path.exists(file_dir_path))

    @staticmethod
    def list_all_directory_file_with_extention(root_dir, extention):
        """
        This method lists all files inside the @root_dir and r
        eturn a list of all files ends with the extention @extention
        """
        files_with_ext = []
        all_files = os.listdir(root_dir)
        for f in all_files:
            if f.endswith(extention):
                files_with_ext.append(os.path.join(root_dir, f))
        return files_with_ext

    @staticmethod
    def copy_directory(src, dest):
        """
        This method copy the folder with its content from source @src to a given destination @dest
        """
        if Common.check_if_file_dir_exists(src):
            shutil.copytree(src, dest)
        else:
            raise DMAException("Either: {}, or {} not exist".format(src, dest))

    @staticmethod
    def load_files_pandas(file, csv=True):
        """
        This methor reads files into a pandas datafram
        TODO: Other datatypes of files (JSON, etc..)
        """
        df = None
        if file.endswith("csv"):
            df = pd.read_csv(file)
        return df

    @staticmethod
    def read_json_file(file_path):
        """
        Read the content of a JSON file and return its data.
        """
        content = None
        with open(file_path, 'r') as file:
            content = json.load(file)
        return content


    @staticmethod
    def save_pandas_df_to_file(df, file, csv=True):
        """
        This methor saves df into a files
        TODO: Other datatypes of files (JSON, etc..)
        """
        if file.endswith("csv"):
            df.to_csv(file)

    @staticmethod
    def write_to_csv(data, filename, header=None):
        """
        This method write the data provided to the CSV file
        filename: name of the file to create (experiment ID)
        header: the header titles of the csv files
        append: if true the data will be appended to the end of the file
        -----
        Returns
        ------
        """
        mode = ("w", "a")[header is None]
        try:
            f = open(filename, mode, newline='')
            writer = csv.writer(f)
            if header is not None:
                writer.writerow(header)
            if data is not None:
                writer.writerow(data)
            f.close()
        except Exception as exp:
            raise Exception("Failed to write \n {} \n to csv file {} in mode {}: {}".format(data, filename, mode, str(exp)))

    @staticmethod
    def write_dataframe_to_csv(df, file_path):
        try:
            df.to_csv(file_path, index=False)
            print("DataFrame successfully written to CSV file:", file_path)
        except Exception as e:
            print("An error occurred while writing to CSV:", e)

    @staticmethod
    def from_dict_of_dict_to_table(matrix):
        """
        It extracts the keys from the first inner dictionary of the matrix and uses them as column headers. 
        It then prints the column headers and a line of dashes. After that, it iterates over each row of the 
        matrix and prints the corresponding values in each column, separated by vertical bars.
        """
        # Extract keys from the first inner dictionary to use as column headers
        columns = list(matrix[next(iter(matrix))].keys())
        # Initialize the table string with column headers
        table = ""
        header = "|".join(columns)
        table += header + "\n"
        table += "-" * len(header) + "\n"
        # Generate each row of the table
        for key, inner_dict in matrix.items():
            row_data = "|".join(str(inner_dict.get(col, "")) if not isinstance(inner_dict.get(col), list) and \
                                isinstance(inner_dict.get(col), int) else str(inner_dict.get(col)) for col in columns)
            table += row_data + "\n"
        return table
