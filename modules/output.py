import re
import sys
import time
from rich.syntax import Syntax
from colorama import Fore, Style
from modules.custom_logger import CustomLogger

logger = CustomLogger("output")

def print_highlighted_response(response):
    console = logger.console
    code_block_pattern = re.compile(r'```(\w+)\n(.*?)```', re.DOTALL)

    def repl(match):
        language = match.group(1).lower()
        code = match.group(2)
        syntax = Syntax(code, language, line_numbers=True)
        return syntax

    pos = 0
    for match in code_block_pattern.finditer(response):
        text_before = response[pos:match.start()]
        console.print(text_before)
        logger.log_and_print(text_before, style="white", skip_print=True)
        code_block = repl(match)
        console.print(code_block)
        logger.log_and_print(match.group(0), style="white", skip_print=True)
        pos = match.end()

    text_after = response[pos:]
    console.print(text_after)
    logger.log_and_print(text_after, style="white", skip_print=True)

def display_response(response):
    if response:
        log_entry = f"GPT-4 Response:"
        logger.log_and_print(log_entry, style="bold cyan")
        print_highlighted_response(response)

def display_spinner(stop_event):
    console = logger.console
    # Uses sys.stdout.write() and .flush() instead of Rich
    # This allows it to be animated instead of written to the screen repeatedly
    # Also uses colorama for colors here

    spinner = ['-', '\\', '|', '/']
    start_time = time.time()
    while not stop_event.is_set():
        for s in spinner:
            elapsed_time = time.time() - start_time
            sys.stdout.write(Fore.BLUE + f'\rWaiting for response... {s} (Time elapsed: {elapsed_time:.2f} seconds)' + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.2)

    log_entry = f"Waiting for response completed (Total time elapsed: {elapsed_time:.2f} seconds)"
    logger.log_and_print(log_entry, log_type="info", style="white", skip_print=True)

    console.print("") # Add a newline character after the spinner stops
