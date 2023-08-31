import app_cli as cli
import modbus_module as modbus
import init_serial as init
from log_config import setup_logging

log = setup_logging('app.log', output_console=False)


def init_serial():
    # get serial port
    available_ports = init.list_serial_ports()

    if available_ports:

        # get the serial port
        port = init.select_serial_port(available_ports)

        log.info(f"Serial port selected: {port}")
        return port
    else:
        log.error("No serial ports found.")
        exit()


def init_modbus(serial_port):
    # initialize modbus
    app_modbus = modbus.ModbusRTUApp(serial_port)
    log.info("Modbus initialized.")
    return app_modbus


def init_cli(app_modbus):
    # initialize cli
    app_cli = cli.app_cli(app_modbus)
    log.info("CLI initialized.")
    return app_cli


def main(app_cli):
    # main function
    log.info("Starting main function.")
    app_cli.interactive_mode()


# main
get_serialPort = init_serial()
app_modbus = init_modbus(get_serialPort)
app_cli = init_cli(app_modbus)
main(app_cli)
