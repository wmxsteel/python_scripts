# Created by alanhu at 8/30/23
import unittest
import sys
import os
from pathlib import Path
import asyncio
from bleak import BleakClient
from bleak import BleakScanner

# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_script_directory)

# Append the parent directory to sys.path
sys.path.append(parent_directory)

from modbus_module import ModbusCustom, ModbusRTUApp
import ble_module as _ble

ble = _ble.ble_module()


async def scan_ble():
    devices = await BleakScanner.discover()
    # 2. Print out the devices with a number next to each.
    for i, device in enumerate(devices, 1):
        print(f"{i}. {device.name} ({device.address})")


async def run(address):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print(service)


async def run_modbus(address):
    async with BleakClient(address) as client:
        # Reading a characteristic
        value = await client.read_gatt_char('characteristic_uuid')
        print(f"Characteristic value: {value}")

        # Writing to a characteristic
        await client.write_gatt_char('characteristic_uuid', bytearray([0x01]))


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.ble = ble

    def test_ble_discovery(self):
        address = "06A483C3-301B-7FF0-5630-2291BCF071D8"
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(address))

    def test_ble_nofication(self):
        ble = self.ble
        address = "06A483C3-301B-7FF0-5630-2291BCF071D8"
        rx_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
        tx_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'

        modbus = ModbusCustom()
        modbus_msg = modbus.build_write_holding_registers(1, 73, [300])
        race_throttle_power = modbus_msg

        read_modbus_msg = modbus.build_read_holding_registers(1, 0, 1)
        controller_output_msg = read_modbus_msg

        send_uuid = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'

        asyncio.run(ble.run(address, rx_uuid, tx_uuid, race_throttle_power, controller_output_msg))


if __name__ == '__main__':
    unittest.main()

# Nordic UART 6E400001-B5A3-F393-E0A9-E50E24DCCA9E
# UART RX Characteristic 6E400002-B5A3-F393-E0A9-E50E24DCCA9E
# UART TX Characteristic 6E400003-B5A3-F393-E0A9-E50E24DCCA9E
