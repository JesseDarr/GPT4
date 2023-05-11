import os

class ExitException(Exception):
    # Raised when the user types 'exit' to exit the application
    pass

def clear_screen():
    # Clear the terminal screen
    if is_windows():
        clear_screen_windows()
    else:
        clear_screen_unix()

def is_windows():
    # Return True if the operating system is Windows, otherwise False
    return os.name == 'nt'

def clear_screen_windows():
    # Clear the terminal screen on Windows
    os.system('cls')

def clear_screen_unix():
    # Clear the terminal screen on Unix-based systems (Linux and macOS)
    os.system('clear')