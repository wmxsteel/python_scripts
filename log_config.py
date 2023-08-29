import os
import logging


def setup_logging(log_file_name='app.log', output_console=True):
    """Configure logging settings."""
    # Ensure log directory exists
    log_dir = 'log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file_name)

    # Configure logging
    if output_console:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s]: %(message)s',
            handlers=[
                logging.FileHandler(log_file_path),
                logging.StreamHandler()  # This will also print logs to the console. Remove if not needed.
            ]
        )
    elif not output_console:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s]: %(message)s',
            handlers=[
                logging.FileHandler(log_file_path)
            ]
        )

    log = logging.getLogger(__name__)
    log.debug("Logging is set up!")
    return log
