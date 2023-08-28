import serial.tools.list_ports


def list_serial_ports():
    """List all available serial ports."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return []

    print("Available serial ports:")
    for i, port in enumerate(ports, start=1):
        print(f"{i}. {port.device}")

    return [port.device for port in ports]


def select_serial_port(available_ports):
    """Let the user select a serial port by entering its name or number."""
    while True:
        selection = input("Enter the name or number of the serial port you want to select: ").strip()

        # Check if user entered a number
        if selection.isdigit():
            idx = int(selection) - 1
            if 0 <= idx < len(available_ports):
                print(f"You selected: {available_ports[idx]}")
                return available_ports[idx]
            else:
                print("Invalid number. Please try again.")
        # Check if user entered a name
        elif selection in available_ports:
            print(f"You selected: {selection}")
            return selection
        else:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    available_ports = list_serial_ports()
    if available_ports:
        select_serial_port(available_ports)
