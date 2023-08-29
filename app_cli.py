import modbus_module as modbus

class app_cli:

    def __init__(self, app_modbus):
        self.app_modbus = app_modbus

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

                self.app_modbus.read_holding_registers(address, count)

            else:
                print(f"Unknown command '{command}'.")



