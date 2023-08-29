import termcolor

import modbus_module as modbus
import dictionary_module as dictionary
from tabulate import tabulate


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

    def interactive_mode(self):
        """Interactive command mode."""
        print("Enter 'exit' to quit the application.")
        while True:
            command = input("Enter command ( (r)ead | (w)rite | (s)ingle | exit ): ").strip().lower()

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
                case 'single':
                    self.write_single()
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

        #write_bac = self.app_modbus.write_single_register(address, value)

        print(f"Write single register: {write_bac}")
        #self.print_tabulate(write_bac)


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
