import re
import sys
import time
from rich.syntax import Syntax
from colorama import Fore, Style
from modules.custom_logger import CustomLogger

logger = CustomLogger("gpt4_shell")  # get ref to singleton logger

def add_syntax_highlighting(match):
    # Adds syntax highlighting to matched code block
    language = match.group(1).lower()
    code = match.group(2)
    syntax = Syntax(code, language, line_numbers=False)
    return syntax

def print_highlighted_response(response):
    # Prints response with syntax-highlighted code blocks
    console = logger.console
    code_block_pattern = re.compile(r'```(\w+)\n(.*?)```', re.DOTALL)

    pos = 0
    for match in code_block_pattern.finditer(response):
        text_before = response[pos:match.start()]
        logger.log_and_print(text_before, style="white")

        code_block = add_syntax_highlighting(match)
        console.print(code_block)  # use console to print so we can have syntax highlighting
        logger.log_and_print(match.group(0), style="white", skip_print=True)

        pos = match.end()

    text_after = response[pos:]
    logger.log_and_print(text_after, style="white")

def display_response(response):
    # Displays GPT-4 response with syntax highlighting for code blocks
    if response:
        log_entry = f"GPT-4 Response:"
        logger.log_and_print(log_entry, style="bold cyan")
        print_highlighted_response(response)

def display_spinner(stop_event):
    # Displays an animated spinner while waiting for a response
    console = logger.console
    start_time = time.time()
    
    elapsed_time = animate_spinner_and_get_elapsed_time(stop_event, start_time)
    
    log_entry = f"Waiting for response completed (Total time elapsed: {elapsed_time:.2f} seconds)"
    logger.log_and_print(log_entry, log_type="info", style="white", skip_print=True)

    console.print("")  # blank line after spinner stops

def animate_spinner_and_get_elapsed_time(stop_event, start_time):
    # Animates spinner using sys.stdout.write() and .flush() and Colorama
    spinner = ['-', '\\', '|', '/']
    elapsed_time = 0
    
    while not stop_event.is_set():
        for s in spinner:
            elapsed_time = time.time() - start_time
            sys.stdout.write(
                Fore.BLUE + f'\rWaiting for response... {s} (Time elapsed: {elapsed_time:.2f} seconds)' + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.2)
    
    return elapsed_time