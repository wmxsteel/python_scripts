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

    def interactive_mode(self):
        """Interactive command mode."""
        print("Enter 'exit' to quit the application.")
        while True:
            command = input("Enter command ( (r)ead | (s)earch | (w)rite | (wr)ingle | exit ): ").strip().lower()

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
                case 's':
                    self.write_single()
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


    def print_tabulate(self, read_bac):
        '''
        @summary: Print the tabulate table
        @param read_bac:
        @return:
        '''

        if read_bac is None:
            return None
        else:
            # print the tabulate table

            for key, value in read_bac.items():
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

                scaled_value = value / scale

                key = color_text(key, "32")
                name = color_text(name, "32")
                # scaled value color red
                scaled_value = color_text(scaled_value, "31")
                units = color_text(units, "35")
                # description color yellow
                description = color_text(description, "33")

                print(tabulate([[key, name, scaled_value, units, description]],
                               headers=['Address', 'Name', 'Value', 'Units', 'Description'], tablefmt='pretty'))

                self.log.info(
                    f"Address: {key}, Name: {name}, Value: {scaled_value}, Units: {units}, Description: {description}")

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
        # self.print_tabulate(write_bac)

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



