import os
import sys
from modules.gpt import get_gpt4_response
from modules.input import get_user_input
from modules.output import display_response
from modules.utils import clear_screen, ExitException
from modules.custom_logger import CustomLogger

def start_input_loop():
    while True:
        try:
            prompt = get_user_input()
            response = get_gpt4_response(prompt, API_KEY)
            display_response(response)
        except ExitException:
            log_message = "Exiting the program."
            logger.log_and_print(log_message, style="bold yellow")
            break
        except KeyboardInterrupt:
            log_message = "Detected keyboard interrupt. Exiting the program."
            logger.log_and_print(log_message, style="bold yellow")
            break
        except Exception as e:
            log_message = f"An unexpected error occurred: {e}"
            logger.log_and_print(log_message, log_type="exception", style="bold red")

if __name__ == '__main__':
    logger = CustomLogger("gpt4_shell")  # Initialize the singleton logger

    API_KEY = os.environ.get('GPT4_API_KEY')
    if not API_KEY:
        log_entry = f"Error: API key not found in environment variables"
        logger.log_and_print(log_entry, log_type="error", style="bold red")
        sys.exit()

    clear_screen()
    start_input_loop()