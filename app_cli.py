import modbus_module as modbus
import dictionary_module as dictionary
from tabulate import tabulate

class app_cli:

    def __init__(self, app_modbus):
        self.app_modbus = app_modbus
        self.bac_dict = dictionary.bac_dictionary()

    def interactive_mode(self):
        """Interactive command mode."""
        print("Enter 'exit' to quit the application.")
        while True:
            command = input("Enter command (readhold/exit): ").strip().lower()

            if command == 'exit':
                print("Exiting application.")
                break
            elif command == 'readhold':
                address = int(input("Enter starting address (default is 0): ") or 0)
                count = int(input("Enter number of registers to read (default is 10): ") or 10)

                read_bac = self.app_modbus.read_holding_registers(address, count)

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

                    print(tabulate([[key, name, scaled_value, units, description]], headers=['Address', 'Name', 'Value', 'Units', 'Description'], tablefmt='orgtbl'))
                 #   print(f"Address:{key} {name} :{scaled_value}{units} Description:{description}")
          #          print(f"{name} Address {address}: {scaled_value}")


