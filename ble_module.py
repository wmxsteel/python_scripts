import asyncio
from bleak import BleakScanner, BleakClient


class ble_module:

    def __init__(self):
        self.notification_dict = {}

    async def ble_scanner(self):
        # 1. Use the bleak library to scan for BLE devices.
        devices = await BleakScanner.discover()

        # 2. Print out the devices with a number next to each.
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device.name} ({device.address})")

        # 3. Prompt the user to select a device by entering its number.
        choice = input("Enter the number of the device you want to select: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(devices):
                selected_device = devices[index]
                print(f"You have selected: {selected_device.name} ({selected_device.address})")
                return selected_device
            else:
                print("Invalid choice. Please select a valid number.")
                return None
        except ValueError:
            print("Please enter a valid number.")
            return None

    async def write_to_ble(self, address, characteristic_uuid, data):
        async with BleakClient(address) as client:
            await client.write_gatt_char(characteristic_uuid, data)

    # Call the test function
    async def discover_services(self, address):
        async with BleakClient(address) as client:
            services = await client.get_services()
            for service in services:
                print(service)

    def notification_handler(self, sender: int, data: bytearray):
        """Callback for BLE notifications."""
        import modbus_module as _modbus
        modbus = _modbus.ModbusCustom()
        # TODO: Parse the data and store it in a dictionary
        parsed_data = modbus.parse_modbus_frame_msg(data)

        notification_dict = self.notification_dict
        notification_dict[sender] = data
        self.notification_dict = notification_dict

    #  print(f"Received data from {sender}: {data}")

    async def run(self, address: str, rx_uuid: str, tx_uuid, write_data=None, read_data=None):
        async with BleakClient(address) as client:
            print(f"Connected: {client.is_connected}")

            loop_counter = 0
            await client.start_notify(rx_uuid, self.notification_handler)

            while loop_counter < 10:

                if write_data is not None:
                    write_data = loop_counter * write_data
                    await client.write_gatt_char(tx_uuid, read_data)
                    print(f"Write Data: {write_data}")

                # Key: 6e400003-b5a3-f393-e0a9-e50e24dcca9e (Handle: 10): Nordic UART TX, Value: bytearray(b'\x01\x10\x00I\x00\x01\xd0\x1f')
                # Key: 6e400003 - b5a3 - f393 - e0a9 - e50e24dcca9e(Handle: 10): Nordic  UART  TX, Value: bytearray(b'\x01\x03\x02\x00\x968*')

                # Write to the characteristic
                # Subscribe to the characteristic

                if read_data is not None:
                    #   await client.read_gatt_char(tx_uuid, read_data)
                    pass
                # Wait for 10 seconds to receive notifications
                # This can be any other condition you need, like a user input or other stop condition
                await asyncio.sleep(3)
                loop_counter += 1
                print(f"Loop counter: {loop_counter}")
            # Stop receiving notifications
            await client.stop_notify(rx_uuid)

            # print out the notification dictionary
            for key, value in self.notification_dict.items():
                print(f"Key: {key}, Value: {value}")
