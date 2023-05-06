import openai
import threading
import os
import re
import sys
import time
import logging
from datetime import datetime
from rich import print as rprint
from rich.console import Console
from rich.syntax import Syntax
from rich.text import Text
from colorama import Fore, Style

class ExitException(Exception):
    pass

def print_highlighted_response(response):
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
        log_and_print(text_before, style="white", skip_print=True)
        code_block = repl(match)
        console.print(code_block)
        log_and_print(match.group(0), style="white", skip_print=True)
        pos = match.end()

    text_after = response[pos:]
    console.print(text_after)
    log_and_print(text_after, style="white", skip_print=True)

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

def log_and_print(message, log_type="info", style="white", skip_print=False):
    if log_type == "error":
        logging.error(message)
        if not skip_print:
            console.print(message, style="bold red")
    elif log_type == "exception":
        logging.exception(message)
        if not skip_print:
            console.print(message, style="bold red")
    else:
        logging.info(message)
        if not skip_print:
            console.print(message, style=style)


def send_to_gpt4(text):
    openai.api_key = API_KEY

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "system", "content": "When providing code, please enclose it in triple backticks with the appropriate language specified."},
        {"role": "user", "content": text}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=6500,
        n=1,
        stop=None,
        temperature=0.7,
    )

    if response.choices:
        message = response['choices'][0]['message']['content'].strip()
        return message

    return "I'm not sure how to respond to that."

def read_input():
    lines = []
    while True:
        line = input()
        if '///' in line:
            line = line.replace('///', '').strip() # remove /// from input and .strip(any white space)
            lines.append(line)
            break
        elif line == 'exit':
            raise ExitException # trying to be proper here
        else:
            lines.append(line)
    return "\n".join(lines)

def display_instructions():
    log_entry = "Enter your prompt (type '///' to submit or 'exit' to quit): "
    log_and_print(log_entry, style="bold green")

def display_spinner(stop_event):
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
    logging.info(log_entry)
    
    console.print("") # Add a newline character after the spinner stops

def clear_screen():
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for Linux and macOS
        os.system('clear')

def get_user_input():
    display_instructions()
    user_input = read_input()
    log_entry = f"User Input: {user_input}"
    logging.info(log_entry)
    return user_input

def get_gpt4_response(prompt):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=display_spinner, args=(stop_event,))
    spinner_thread.daemon = True

    console.print("")  # Add a newline character before starting the spinner thread
    spinner_thread.start()

    try:
        response = send_to_gpt4(prompt)
    except Exception as e:
        error_message = f"Error: {e}"
        logging.error(error_message)
        console.print(f"\n{error_message}", style='red')
        response = None
    finally:
        stop_event.set()
        spinner_thread.join()
        console.print("\r", end="")
        sys.stdout.flush()

    console.print("")  # Add a newline character after the spinner thread has finished
    return response

def display_response(response):
    if response:
        log_entry = f"GPT-4 Response:"
        log_and_print(log_entry, style="bold cyan")
        print_highlighted_response(response)

def start_input_loop():
    while True:
        try:
            prompt = get_user_input()
            response = get_gpt4_response(prompt)
            display_response(response)
        except ExitException:
            log_message = "Exiting the program."
            log_and_print(log_message, style="bold yellow")
            break
        except KeyboardInterrupt:
            log_message = "Detected keyboard interrupt. Exiting the program."
            log_and_print(log_message, style="bold yellow")
            break
        except Exception as e:
            log_message = f"An unexpected error occurred: {e}"
            log_and_print(log_message, log_type="exception", style="bold red")

if __name__ == '__main__':
    console = Console() # Init Rich Console - used for colors and syntax highlighting
    setup_logger()
    clear_screen()
    
    API_KEY = os.environ.get('GPT4_API_KEY')
    if not API_KEY:
        log_entry = f"Error: API key not found in environment variables"
        log_and_print(log_entry, log_type="error", style="bold red")
        sys.exit()    

    start_input_loop()