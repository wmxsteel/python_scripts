import serial.tools.list_ports


def list_serial_ports():
    """List all available serial ports."""
    ports = list(serial.tools.list_ports.comports())

    bluetooth_ports = [port for port in ports if "Bluetooth" in port.name]
    other_ports = [port for port in ports if "Bluetooth" not in port.name]

    if not ports:
        print("No serial ports found.")
        return []

    print("Available serial ports:")
    for i, port in enumerate(other_ports, start=1):
        print(f"{i}. {port.device}")

    print('\nAvailable bluetooth ports:')
    # Start numbering of Bluetooth ports after the serial ports
    for i, port in enumerate(bluetooth_ports, start=len(other_ports) + 1):
        print(f"{i}. {port.device}")

    return other_ports + bluetooth_ports  # combining both lists


def select_serial_port(available_ports):
    """Let the user select a serial port by entering its name or number."""
    while True:
        selection = input("\nEnter the name or number of the serial port you want to select: ").strip()
        if selection.isdigit():
            idx = int(selection) - 1
            if 0 <= idx < len(available_ports):
                print(f"You selected: {available_ports[idx].device}")
                return available_ports[idx].device
            else:
                print("Invalid number. Please try again.")
        elif any(port.device == selection for port in available_ports):
            print(f"You selected: {selection}")
            return selection
        else:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    available_ports = list_serial_ports()
    if available_ports:
        select_serial_port(available_ports)
