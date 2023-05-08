import os
import logging
from datetime import datetime
from rich.console import Console
from modules.utils import UnexpectedErrorException

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CustomLogger(logging.Logger, metaclass=Singleton):

    def __init__(self, name, level=logging.INFO):
        super().__init__(name, level)

        self.console = Console()
        self._create_log_file()

    def _create_log_file(self):
        # Moved log file creation into a separate function for SRP
        log_directory = "logs"
        os.makedirs(log_directory, exist_ok=True)
        log_filename = datetime.now().strftime("%m-%d-%Y_%H-%M-%S.log")
        log_filepath = os.path.join(log_directory, log_filename)

        file_handler = logging.FileHandler(log_filepath)
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d | %(message)s', datefmt='%Y-%m-%d | %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    def log_and_print(self, message, log_type="info", style="white", skip_print=False):
        # Use map to determine what style we are
        log_func_map = {
            "error": self.error,
            "exception": self.exception,
            "info": self.info
        }
        log_func = log_func_map.get(log_type)

        log_func(message)
        if not skip_print:
            self.console.print(message, style=style)

logging.setLoggerClass(CustomLogger)