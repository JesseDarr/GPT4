import os

class ExitException(Exception):
    pass

class UnexpectedErrorException(Exception):
    pass

def clear_screen():
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for Linux and macOS
        os.system('clear')    