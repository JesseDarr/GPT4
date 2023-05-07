from modules.gpt import get_gpt4_response
from modules.input import get_user_input
from modules.output import display_response
from modules.utils import ExitException, UnexpectedErrorException
from modules.custom_logger import CustomLogger

logger = CustomLogger("gpt4_shell") # get ref to singleton logger

def start_input_loop(api_key):
    while True:
        try:
            prompt = get_user_input()
            response = get_gpt4_response(prompt, api_key)
            display_response(response)
        except ExitException:
            raise
        except KeyboardInterrupt:
            raise
        except Exception as e:
            raise UnexpectedErrorException from e
