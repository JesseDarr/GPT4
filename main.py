# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
from rich.console import Console
from rich.text import Text

# Local imports
from modules.gpt import get_gpt4_response
from modules.input import get_user_input
from modules.output import log_and_print, display_response
from modules.utils import clear_screen, setup_logger, ExitException

def start_input_loop(console):
    while True:
        try:
            prompt = get_user_input(console)
            response = get_gpt4_response(prompt, console, API_KEY)
            display_response(response, console)
        except ExitException:
            log_message = "Exiting the program."
            log_and_print(log_message, style="bold yellow", console=console)
            break
        except KeyboardInterrupt:
            log_message = "Detected keyboard interrupt. Exiting the program."
            log_and_print(log_message, style="bold yellow", console=console)
            break
        except Exception as e:
            log_message = f"An unexpected error occurred: {e}"
            log_and_print(log_message, log_type="exception", style="bold red", console=console)

if __name__ == '__main__':
    console = Console() # Init Rich Console - used for colors and syntax highlighting
    setup_logger()
    clear_screen()
    
    API_KEY = os.environ.get('GPT4_API_KEY')
    if not API_KEY:
        log_entry = f"Error: API key not found in environment variables"
        log_and_print(log_entry, log_type="error", style="bold red", console=console)
        sys.exit()    

    start_input_loop(console)