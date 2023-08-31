import termcolor
import modbus_module as modbus
import dictionary_module as dictionary
from tabulate import tabulate
from log_config import setup_logging


# Colorize text function
def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


# color codes
# 30 - black
# 31 - red
# 32 - green
# 33 - yellow
# 34 - blue
# 35 - magenta
# 36 - cyan
# 37 - white


class app_cli:

    def __init__(self, app_modbus):

        self.app_modbus = app_modbus
        self.bac_dict = dictionary.bac_dictionary()
        self.lastaddress = 0
        self.lastvalue = 0
        self.log = setup_logging('app_cli.py', output_console=False)
        self.comm = 'Serial'  # or 'BLE'

    def interactive_mode(self):
        """Interactive command mode."""
        print("Enter 'exit' to quit the application.")
        while True:
            command = input(
                "Enter command ( (r)ead | (s)earch | (w)rite | (wr)ingle | (c)onnection | exit ): ").strip().lower()

            match command:
                case 'exit':
                    print("Exiting application.")
                    break
                case 'read':
                    self.read_holdingregs()
                case 'r':
                    self.read_holdingregs()
                case 'write':
                    self.write_holdingregs()
                case 'w':
                    self.write_holdingregs()
                case 'wr':
                    self.write_single()
                case 's':
                    self.search_param_name()
                case 'c':
                    #  self.page_comm_interface()
                    self.select_comm_interface()

                case 'help':
                    self.help()
                case _:
                    print("Invalid command.")

    def input_address(self, address):
        if address == '':
            address = self.lastaddress
        else:
            address = int(address)
            self.lastaddress = address
        return address

    def read_holdingregs(self):
        """
        Read holding registers from the device.
        """
        address = int(input(f"Enter starting address (default is {self.lastaddress}): "))
        #     address = self.input_address(address)
        count = int(input("Enter number of registers to read (default is 10): ") or 10)
        read_bac = self.app_modbus.read_holding_registers(address, count)
        self.print_tabulate(read_bac)

    def list_parse(self, bac_data):
        '''
        @summary: Build a table from the bac_data
        scaled_value = value / scale or value * scale
        Depending on whether its a read or write

        @param bac_data:
        @return:
        '''
        if bac_data is None:
            return None
        else:
            last_key, last_value = self.get_mod_dict_type(bac_data)

        # the last value is either 'read' or 'write'
        # if read then divide by scale
        # if write then multiply by scale
        #
    def list_build(self, bac_data, last_key, mode="read"):
        '''
        @summary: Parse the list from the bac_data and append more details to the list
        @param bac_data:
        @param mode:
        @return:
        '''

        for key, value in bac_data.items():
            if key == last_key:
                break
            bac_param = self.bac_dict.lookup_row_by_address(address=key)
            name = bac_param["name"]
            description = bac_param["description"]
            scale = bac_param["scale"]
            units = bac_param["units"]
            bitfield = bac_param["bitfield"]

            # check if scale is not a string
            if isinstance(scale, str):
                if scale is 'bit vector' and bitfield is '{}':
                    self.bac_dict.build_bitvector(address=key)
            elif isinstance(scale, float):
                scale = float(scale)
            else:
                scale = int(scale)

    # Should build a table before that
    # Print Tabulate should be the last step
    def print_tabulate(self, read_bac):
        '''
        @summary: Print the tabulate table
        @param read_bac:
        @return:
        '''

        # TODO: Take into account that the last key is the 'mode' key. Need to account for that otherwise program will crash.

        if read_bac is None:
            return None
        else:
            last_key, last_value = self.get_mod_dict_type(read_bac)
            scaled_value = 0
            scale = 0

            # the last value is either 'read' or 'write'

            # read thru the dict excluding the last entry

            for key, value in read_bac.items():
                if key == last_key:
                    break
                bac_param = self.bac_dict.lookup_row_by_address(address=key)
                name = bac_param["name"]
                description = bac_param["description"]
                scale = bac_param["scale"]
                units = bac_param["units"]


                # check if scale is not a string
                if isinstance(scale, str):
                    scale = int(1)
                elif isinstance(scale, float):
                    scale = float(scale)
                else:
                    scale = int(scale)

                ## Color Outputs ##

                key = color_text(key, "32")
                name = color_text(name, "32")
                units = color_text(units, "35")
                # description color yellow
                description = color_text(description, "33")

                ## If write then do not add use the value column ##

                header_table = ['Address', 'Name', 'Value', 'Units', 'Description']

                if last_value == 'write':
                    scaled_value = value * scale
                elif last_value == 'read':
                    scaled_value = value / scale

                scaled_value = color_text(scaled_value, "31")
                column_table = [key, name, scaled_value, units, description]

                print(tabulate([column_table],
                               headers=header_table, tablefmt='pretty'))

                self.log.info(
                    f"Address: {key}, Name: {name}, Value: {scaled_value}, Units: {units}, Description: {description}")

    def get_mod_dict_type(self, read_bac):
        # print the tabulate table
        len_dict = len(read_bac)
        # read the last key in the dictionary and get the value
        last_key = list(read_bac.keys())[-1]
        last_value = read_bac[last_key]
        return last_key, last_value

    def print_tabulate_df(self, param_df):
        '''
        @param param_df:
        @summary: Print the tabulate table
        @param read_bac:
        @return:
        '''

        if param_df is None:
            return None
        else:
            # print the tabulate table

            for index, row in param_df.iterrows():
                address = row["Address"]
                name = row["Name"]
                description = row["Description"]
                scale = row["Scale"]
                units = row["Units"]

                # check if scale is not a string
                if isinstance(scale, str):
                    scale = int(1)
                elif isinstance(scale, float):
                    scale = float(scale)
                else:
                    scale = int(scale)

                address = int(address)
                address = color_text(address, "32")

                name = color_text(name, "32")
                # scaled value color red
                units = color_text(units, "35")
                # description color yellow
                description = color_text(description, "33")
                print(tabulate([[address, name, units, description]],
                               headers=['Address', 'Name', 'Units', 'Description'], tablefmt='pretty'))

                # print(tabulate([[address, name, scaled_value, units, description]],
                #                headers=['Address', 'Name', 'Value', 'Units', 'Description'], tablefmt='pretty'))

                self.log.info(
                    f"Address: {address}, Name: {name}, Units: {units}, Description: {description}")

    def write_single(self):
        '''
        @summary: Write a single register to the device.
        @return:
        '''

        address = int(input(f"Enter starting address (default is {self.lastaddress}): "))
        #    address = self.input_address(address)
        #   address = self.input_address(address)
        value = int(input("Enter value to write: "))

        # get the scale
        bac_param = self.bac_dict.lookup_row_by_address(address=address)
        scale = bac_param["scale"]
        # check if scale is not a string
        if isinstance(scale, str):
            scale = int(1)
        elif isinstance(scale, float):
            scale = float(scale)
        else:
            scale = int(scale)

        # scale the value
        value = value * scale

        write_bac = self.app_modbus.modbus_handler(address, "write single", value=value)

        # write_bac = self.app_modbus.write_single_register(address, value)

        print(f"Write single register: {write_bac}")
        self.print_tabulate(write_bac)

    def write_holdingregs(self):
        """
        Write holding registers to the device.
        """
        address = int(input("Enter starting address (default is 0): ") or 0)
        count = int(input("Enter number of registers to write (default is 1): ") or 1)
        value = int(input("Enter value to write: "))

        write_bac = self.app_modbus.write_holding_registers(address, count, value)
        self.print_tabulate(write_bac)

    def help(self):
        print("Help")

    def search_param_name(self):
        '''
        @summary: Search the parameter name
        @return:
        '''
        name = input("Enter parameter name: ")
        results = self.bac_dict.search_bac_dict_name(name=name)
        self.print_tabulate_df(results)

    def page_comm_interface(self):
        '''
        @summary: Prompt the user to select a communication interface
        @return:
        '''
        print("Select a communication interface:")
        print("1. Serial")
        print("2. BLE")
        print("3. Exit")

        choice = input("Enter the number of the interface you want to select: ")
        try:
            index = int(choice) - 1
            if 0 <= index < 3:
                if index == 0:
                    self.comm = 'Serial'
                    print(f"You have selected: {self.comm} interface")
                elif index == 1:
                    self.comm = 'BLE'
                    print(f"You have selected: {self.comm} interface")
                elif index == 2:
                    print("Exiting application.")
                    exit()
                else:
                    print("Invalid choice. Please select a valid number.")
                    self.interactive_mode()
            else:
                print("Invalid choice. Please select a valid number.")

        except ValueError:
            print("Please enter a valid number.")

    def get_comm_interface(self):
        return self.comm

    def select_comm_interface(self):
        import init_serial as init_serial

        ports = init_serial.list_serial_ports()
        init_serial.select_serial_port(ports)
