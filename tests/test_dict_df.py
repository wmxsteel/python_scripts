# Created by alanhu at 8/28/23
import unittest
import sys
import os
from pathlib import Path

# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_script_directory)

# Append the parent directory to sys.path
sys.path.append(parent_directory)
import pandas as pd
from dictionary_module import bac_dictionary


def lookup_row_by_address(df, address):
    """
    Function to lookup a row in the DataFrame based on the Address column.

    Parameters:
    - df: pandas DataFrame containing the data
    - address: address value to lookup

    Returns:
    - Row(s) in the DataFrame matching the specified address, or None if no match is found.
    """
    matching_rows = df[df["Address"] == address]

    if not matching_rows.empty:
        return matching_rows
    else:
        return None


def test_parse_print_parameter_values(parameter_values):

    address = parameter_values["address"]
    name = parameter_values["name"]
    scale = parameter_values["scale"]
    units = parameter_values["units"]
    description = parameter_values["description"]
    key = parameter_values["key"]
    access_level = parameter_values["access_level"]
    bitfield = parameter_values["bitfield"]

    print(f"{name} Address:{address} has scale {scale} and units {units}. Description: {description}")



    # print key and value in dictionary
    for key, value in parameter_values.items():
        print(f"{key}: {value}")


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # Load the ASIObjectDictionary.xlsx into a pandas DataFrame
        self.dictionary = bac_dictionary()
        pass


    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_parse_bac_read_address(self):
        # Read the data from the Excel file
        # Load the newly provided XLSX file
        dictionary = bac_dictionary()
        parameter_values = dictionary.get_values_from_address(address=0)

        # print key and value in dictionary
     #   for key, value in parameter_values.items():
     #       print(f"{key}: {value}")
        # Read the data from the Excel file
        # Test read 10 registers
        test_parse_print_parameter_values(parameter_values)
        dictionary.bac_read(address=0, value=10)
        # Feed address and value into dictionary parser and get the name and value

        # Read the data from the Excel file

    def test_search_bac_dict_name(self):
        import dictionary_module as dm
        import app_cli as app_cli
        import modbus_module as modbus_module
        modbus = modbus_module.ModbusRTUApp('COM3')
        bac_dict = dm.bac_dictionary()

        # search the bac dict by name
        results = bac_dict.search_bac_dict_name(name="Motor")
        print(results)

        cli = app_cli.app_cli(app_modbus=modbus)
        cli.print_tabulate_df(results)
        # return as pandas dataframe
        # send to CLI and print as tabuate table

if __name__ == '__main__':
    unittest.main()
