"""Deny Of Service Test Tool
This tool is only for testing purposes.

Usage:
    %s <config_file>
    %s -h | --help

Options:
    -h --help                   Show this screen.
"""

# ===== Imports ===== #
# Local imports
import os
import sys
import logging
from json import (load,
                  JSONDecodeError)
from typing import (Optional,
                    NoReturn)

# Third party imports
# from socket import (socket,
#                     AF_INET,
#                     SOCK_STREAM,)

# ===== Constants ===== #
ARGS: list[str] = sys.argv
LOGGING: dict[str, str] = {
    'level': 'DEBUG',
    'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    'stream': sys.stdout
}

# ===== Logging ===== #
logging.basicConfig(level=LOGGING['level'],
                    format=LOGGING['format'],
                    datefmt=LOGGING['datefmt'],
                    stream=LOGGING['stream'])

# ===== Functions ===== #
def exit_error() -> NoReturn:
    """Exit the script with an error message.
    """
    logging.exception('Fatal error, exiting')
    os._exit(1)

def load_config(config_file: Optional[str] = 'config.json', *,
                encoding: Optional[str] = 'utf-8') -> dict:
    """Load the configuration file.

    Args:
        config_file (str, optional): The configuration file to use. Defaults to 'config.json'.
        encoding (str, optional): The encoding to use. Defaults to 'utf-8'.
    
    Raises:
        FileNotFoundError: If the configuration file does not exist.


    Returns:
        dict: The configuration file as a dictionary.
    """
    _return: dict[str, str | int] = {}

    if not os.path.exists(config_file):
        logging.error('Configuration file %s does not exist.', config_file)
        exit_error()

    with open(config_file, 'r', encoding=encoding) as file:
        try:
            _return = load(file)

        except JSONDecodeError as error:
            logging.error('Error loading configuration file: %s', error)

        finally:
            file.close()

    return _return

def check_config(config: dict) -> tuple[bool, list[str]]:
    """Check the configuration file.

    Args:
        config (dict): The configuration file to check.

    Returns:
        bool: True if the configuration file is valid, False otherwise.
    """
    _return: bool = True
    if not isinstance(config, dict):
        logging.error('Configuration file is not a dictionary.')
        return False

    if 'host' not in config:
        logging.error('Configuration file does not contain a host.')
        _return = False

    if 'port' not in config:
        logging.error('Configuration file does not contain a port.')
        _return = False

    if 'payload' not in config:
        logging.error('Configuration file does not contain a payload. (It can be empty)')
        _return = False

    return _return

def param_handler() -> str:
    """Handle the parameters passed to the script.
    """

    args: list[str] = ARGS[1:]
    logging.debug('Arguments: %s', args)

    if not args:
        logging.error('No arguments passed.')
        exit_error()

    if len(args) != 1:
        logging.error('Invalid number of arguments. Must be only one.'
                      'Either the configuration file or the help flag.')
        exit_error()

    if args[0] in ['-h', '--help']:
        print(__doc__ % (ARGS[0], ARGS[0]))
        sys.exit(0)

    return args[0]



# ===== Class ===== #
class DOS:
    """Main class for the DOS attack.
    """

# ===== Main ===== #
def main():
    """Main function for the DOS attack tool.
    """
    config_file: str = param_handler()
    config = load_config(config_file)
    if not check_config(config):
        logging.error('Configuration file is not valid.')
        return


if __name__ == '__main__':
    main()
