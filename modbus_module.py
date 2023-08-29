from pymodbus.client import ModbusSerialClient


class ModbusRTUApp:
    def __init__(self, port):
        # Default serial port parameters
        self.port = port
        self.baudrate = 115200
        self.parity = 'N'
        self.stopbits = 1
        self.bytesize = 8

        self.slave = 1
        # Initialize Modbus client with the default parameters
        self.client = ModbusSerialClient(
            port=self.port,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize
        )

    def serial_configure(self):
        """Configure serial port parameters and return them."""
        print("Enter port (e.g., COM1 or /dev/ttyUSB0): ")
        port = input(f"{self.port}")
        baudrate = int(input("Enter baud rate (default is 9600): ") or 115200)
        parity = input("Enter parity (N/E/O, default is N): ") or 'N'
        stopbits = int(input("Enter number of stop bits (default is 1): ") or 1)
        bytesize = int(input("Enter number of data bits (default is 8): ") or 8)
        slave = int(input("Enter slave ID (default is 1): ") or 1)

        return port, baudrate, parity, stopbits, bytesize, slave

    def set_serial_parameters(self, port, baudrate, parity, stopbits, bytesize, slave, ModbusSerialClient):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.slave = slave

        client = ModbusSerialClient(
            method='rtu',
            port=self.port,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize
        )

    def read_holding_registers(self, address, count, slave):
        """Read Modbus RTU holding registers."""
        if not self.client.is_socket_open():
            self.client.connect()

        response = self.client.read_holding_registers(address, count, slave=self.slave)

        if not response.isError():
            for idx, value in enumerate(response.registers):
                print(f"Address {address + idx}: {value}")
        else:
            print("Error reading Modbus data.")

        self.client.close()
