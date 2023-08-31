from pymodbus.client import ModbusSerialClient
import struct
import serial


class ModbusCustom:

    def __init__(self):
        pass

    def calculate_crc(self, data):
        """Calculate CRC-16 for Modbus.
        @param data:
        @return:
        """
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    def build_read_holding_registers(self, slave_address, start_address, count):
        # Frame the modbus request
        function_code = 0x03
        message = struct.pack('>B B H H', slave_address, function_code, start_address, count)

        # Append CRC to the message
        crc = self.calculate_crc(message)
        message += struct.pack('<H', crc)

        return message

        # Send the request over serial port

    def build_write_holding_registers(self, slave_address, start_address, values):
        # Frame the modbus request
        function_code = 0x10
        quantity = len(values)
        byte_count = quantity * 2
        message = struct.pack('>B B H H B', slave_address, function_code, start_address, quantity, byte_count)

        # Add the register values to the message
        for value in values:
            message += struct.pack('>H', value)

        # Append CRC to the message
        crc = self.calculate_crc(message)
        message += struct.pack('<H', crc)

        return message



    # Read the response (we're assuming a response with count * 2 bytes of data + 5 bytes overhead)
    #       response = ser.read(5 + count * 2)

    # Extract and return the data part of the response (excluding address, function code, byte count, and CRC)


#       return response[3:-2]


class ModbusRTUApp:
    def __init__(self, port):
        # Default serial port parameters
        self.port = port
        self.baudrate = 115200
        self.parity = 'N'
        self.stopbits = 1
        self.bytesize = 8

        self.slave = 2
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

    def set_serial_parameters(self, port, baudrate, parity, stopbits, bytesize, slave, modbusSerialClient):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.slave = slave

        client = modbusSerialClient(
            method='rtu',
            port=self.port,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize
        )

        self.client = client

    def modbus_handler(self, address, command, count=1, value=0):
        """Handle Modbus RTU commands."""
        holding_registers_dict = {}
        response = None

        # Connect to the serial port
        try:
            if not self.client.is_socket_open():
                self.client.connect()
        except:
            print("Error connecting to serial port.")
            return None
        else:
            print("Connected to serial port.")
        finally:
            print("Done.")

        # Handle commands
        match command:
            case "read single":
                response = self.client.write_registers(address, count=1, slave=self.slave)
                holding_registers_dict["mode"] = "read"
            case "read multiple":
                response = self.client.read_holding_registers(address, count, slave=self.slave)
                holding_registers_dict["mode"] = "read"
            case "write single":
                response = self.client.write_registers(address, value, slave=self.slave)
                holding_registers_dict["mode"] = "write"
            case "write multiple":
                response = self.client.write_registers(address, value, slave=self.slave)
                holding_registers_dict["mode"] = "write"

        if not response.isError():
            for idx, value in enumerate(response.registers):
                # TODO: Feed into dictionary parser
                holding_registers_dict[address + idx] = value
        else:
            print("Error reading Modbus data.")

        self.client.close()

        if not holding_registers_dict:
            return None
        else:
            return holding_registers_dict

    def read_holding_registers(self, address, count):
        """Read Modbus RTU holding registers."""

        # Append read values to a dictionary
        read_holding_registers_dict = {}

        if not self.client.is_socket_open():
            self.client.connect()

        response = self.client.read_holding_registers(address, count, slave=self.slave)

        if not response.isError():
            for idx, value in enumerate(response.registers):
                # TODO: Feed into dictionary parser
                read_holding_registers_dict[address + idx] = value
            # print(f"Address {address + idx}: {value}")
            read_holding_registers_dict["mode"] = "read"

        else:
            print("Error reading Modbus data.")

        self.client.close()

        if not read_holding_registers_dict:
            return None
        else:
            return read_holding_registers_dict

    def write_single_register(self, address, value):
        """Write a single Modbus RTU holding register."""

        # Append read values to a dictionary
        write_single_register_dict = {}

        if not self.client.is_socket_open():
            self.client.connect()

        # Get the scale value from the dictionary

        response = self.client.write_registers(address, value, slave=self.slave)

        if not response.isError():
            for idx, value in enumerate(response.registers):
                write_single_register_dict[address + idx] = value
            write_single_register_dict["mode"] = "write"
            return write_single_register_dict
            # print(f"Address {address + idx}: {value}")

    def write_holding_registers(self, address, count, value):
        """Write Modbus RTU holding registers."""

        # Append read values to a dictionary
        write_holding_registers_dict = {}

        if not self.client.is_socket_open():
            self.client.connect()

        response = self.client.write_registers(address, count, value, slave=self.slave)

        if not response.isError():
            for idx, value in enumerate(response.registers):
                write_holding_registers_dict[address + idx] = value
            write_holding_registers_dict["mode"] = "write"
            return write_holding_registers_dict
            # print(f"Address {address + idx}: {value}")
        else:
            print("Error writing Modbus data.")
