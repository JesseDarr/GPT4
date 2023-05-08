from modules.gpt import wait_for_query_show_spinner
from modules.input import get_user_input
from modules.output import display_response
from modules.utils import ExitException, UnexpectedErrorException
from modules.custom_logger import CustomLogger

logger = CustomLogger("gpt4_shell") # get ref to singleton logger

def run_main_loop(api_key):
    # Start the main input loop for the application.
    # Handles user input, queries the GPT-4 model, and displays the response.
    while True:
        try:
            prompt = get_user_input()
            response = wait_for_query_show_spinner(prompt, api_key)
            display_response(response)
        except ExitException:
            raise
        except KeyboardInterrupt:
            raise
        except Exception as e:
            raise UnexpectedErrorException(f"An unexpected error occurred: {e}") from e
