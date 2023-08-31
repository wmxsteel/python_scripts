import asyncio
from bleak import BleakScanner


async def ble_scanner():
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



# Call the test function
