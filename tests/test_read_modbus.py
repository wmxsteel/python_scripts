# Created by alanhu at 8/30/23
import unittest
import sys
import os
from pathlib import Path
import serial
import struct

# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_script_directory)

# Append the parent directory to sys.path
sys.path.append(parent_directory)

from modbus_module import ModbusCustom


def write_frame_to_serial(frame, port='/dev/cu.usbserial-0001'):
    """
    Writes a frame to the given serial port.

    Args:
    - frame (bytes): The frame to send.
    - port (str): Serial port to use (default is '/dev/ttyS0').
    """

    # Configure the serial connection
    ser = serial.Serial(
        port=port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    # Ensure the serial port is open
    if not ser.isOpen():
        ser.open()

    # Write the frame to the serial device
    ser.write(frame)

    # Close the serial port when done
    ser.close()


class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_build_modbus_msg_read(self):
        # 1. Build the message
        modbus = ModbusCustom()
        modbus_msg = modbus.build_read_holding_registers(1, 0, 1)
        controller_output_msg = modbus_msg

        print(controller_output_msg)

    def test_build_modbus_msg_write(self):
        # 1. Build the message
        modbus = ModbusCustom()
        modbus_msg = modbus.build_write_holding_registers(1, 73, [0x2500])
        race_throttle_power = modbus_msg
        print(race_throttle_power)

    def test_build_modbus_msg_write_serial(self):
        # 1. Build the message
        modbus = ModbusCustom()
        modbus_msg = modbus.build_write_holding_registers(1, 73, [3000])
        race_throttle_power = modbus_msg
        print(race_throttle_power)
        write_frame_to_serial(race_throttle_power)


if __name__ == '__main__':
    unittest.main()
