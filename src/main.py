"""Deny Of Service Test Tool
This tool is only for testing purposes.

Usage:
    main.py --config-file <config_file>

Options:
    -h --help                   Show this screen.
    --config-file <config_file> Path to the configuration file.
"""

# ===== Imports ===== #
# Local imports
import os
import logging
from json import (load,
                  JSONDecodeError)
from typing import Optional

# Third party imports
# from socket import (socket,
#                     AF_INET,
#                     SOCK_STREAM,)

# ===== Constants ===== #
CONFIG_FILE: str | None = None

# ===== Functions ===== #
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
        raise FileNotFoundError

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

def param_handler() -> None:
    """Handle the parameters passed to the script.

    Raises:
        NotImplementedError: If the function is not implemented.
    """
    raise NotImplementedError

# ===== Class ===== #
class DOS:
    """Main class for the DOS attack.
    """
    def __init__(self) -> None:
        raise NotImplementedError


# ===== Main ===== #
def main():
    """Main function for the DOS attack tool.

    Raises:
        NotImplementedError: If the function is not implemented.
    """
    param_handler()
    config = load_config(CONFIG_FILE)
    if not check_config(config):
        logging.error('Configuration file is not valid.')
        return


if __name__ == '__main__':
    main()
