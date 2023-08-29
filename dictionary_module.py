import os
from typing import Any

import pandas as pd
from numpy import ndarray
from pandas.core.arrays import ExtensionArray


class bac_dictionary:

    def __init__(self):
        # Load the ASIObjectDictionary.xlsx into a pandas DataFrame

        # Get the directory of the current script
        current_script_directory = os.path.dirname(os.path.abspath(__file__))

        bac_dictionary_file = "ASIObjectDictionary.xlsx"
        path_xlsx = current_script_directory + "/" + bac_dictionary_file

        df_asi = pd.read_excel(path_xlsx)
        self.temp_bac_parameters = None
        self.df_asi = df_asi

    def lookup_row_by_address(self, address):
        """Lookup rows in a DataFrame based on the Address column."""
        df = self.df_asi
        asi_parameter_values: ExtensionArray | ndarray | Any = df[df["Address"] == address].values
        # return as a dict
        dict_asi_parameter_values = {
            "address": asi_parameter_values[0][0],
            "name": asi_parameter_values[0][1],
            "scale": asi_parameter_values[0][2],
            "units": asi_parameter_values[0][3],
            "description": asi_parameter_values[0][4],
            "key": asi_parameter_values[0][5],
            "access_level": asi_parameter_values[0][6],
            "bitfield": asi_parameter_values[0][7]
        }

        return dict_asi_parameter_values

    def scale_value(self, address, value, mode="read"):

        asi_parameter_values = self.lookup_row_by_address(address)

        # get scale
        scale = asi_parameter_values["scale"]

        # check if scale is string
        if isinstance(scale, str):
            scale = int(1)
        else:
            # transform value into float
            scaled_value = float(value)
            float_scale = float(scale)

        match mode:
            case "read":
                # if read then divide the value by scale
                scaled_value = scaled_value / float_scale
            case "write":
                # if write then multiply the value by scale
                scaled_value = scaled_value * float_scale

        return scaled_value

    def bac_read(self, address, value):

        df = self.df_asi
        bac_address_values = df[df["Address"] == address].values
        self.temp_bac_parameters = bac_address_values

        scaled_value = self.scale_value(address, value, mode="read")
        name = bac_address_values["Name"]
        description = bac_address_values["Description"]
        units = bac_address_values["Units"]
        access_level = bac_address_values["AccessLevel"]
        address = bac_address_values["Address"]
        scale = bac_address_values["Scale"]
        bitfield = bac_address_values["Bitfield"]

        bac_values_dict = {
            "name": name,
            "description": description,
            "units": units,
            "access_level": access_level,
            "address": address,
            "scale": (scale),
            "bitfield": bitfield,
            "scaled_value": scaled_value
        }

        return bac_values_dict

        return parsed_values

    def get_values_from_address(self, address):
        """
        Function to lookup a row in the DataFrame based on the Address column.

        Parameters:
        - df: pandas DataFrame containing the data
        - address: address value to lookup

        Returns:
        - Row(s) in the DataFrame matching the specified address, or None if no match is found.
        """
        bac_address_values = self.df_asi.iloc[address].values

        # check if
        address = int(bac_address_values[0])
        name = bac_address_values[1]
        scale = bac_address_values[2]
        units = bac_address_values[3]
        description = bac_address_values[4]
        key = bac_address_values[5]
        access_level = bac_address_values[6]
        bitfield = bac_address_values[7]
        bac_values = {
            "address": address,
            "name": name,
            "scale": float(scale),
            "units": units,
            "description": description,
            "key": key,
            "access_level": access_level,
            "bitfield": bitfield
        }

        if bac_address_values is not None:
            return bac_values
        else:
            return None

