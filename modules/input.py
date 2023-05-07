from modules.utils import ExitException
from modules.custom_logger import CustomLogger

logger = CustomLogger("gpt4_response")

def get_user_input():
    display_instructions()
    user_input = read_input()
    log_entry = f"User Input: {user_input}"
    logger.log_and_print(log_entry, skip_print=True)
    return user_input

def read_input():
    lines = []
    while True:
        line = input()
        if '///' in line:
            line = line.replace('///', '').strip()
            lines.append(line)
            break
        elif line == 'exit':
            raise ExitException
        else:
            lines.append(line)
    return "\n".join(lines)

def display_instructions():
    log_entry = "Enter your prompt (type '///' to submit or 'exit' to quit): "
    logger.log_and_print(log_entry, style="bold green")