from datetime import datetime

class ExitException(Exception):
    pass

def setup_logger():
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)
    log_filename = datetime.now().strftime("%m-%d-%Y_%H-%M-%S.log")
    log_filepath = os.path.join(log_directory, log_filename)

    logging.basicConfig(
        filename=log_filepath,
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d | %(message)s',
        datefmt='%Y-%m-%d | %H:%M:%S'
    )

def clear_screen():
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for Linux and macOS
        os.system('clear')    