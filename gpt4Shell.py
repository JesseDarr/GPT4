import openai
import threading
import os
import sys
import time
import logging
from datetime import datetime
from colorama import Fore, Style

class ExitException(Exception):
    pass

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

def log_and_print(message, log_type="info", color=Fore.WHITE):
    if log_type == "error":
        logging.error(message)
    elif log_type == "exception":
        logging.exception(message)
    else:
        logging.info(message)

    print(color + message + Style.RESET_ALL)

def send_to_gpt4(text):
    openai.api_key = API_KEY

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=6500,    # 8k max
        n=1,                # number of responses
        stop=None,
        temperature=0.7,    # 0-1, creativeness/randomness value, 1 = more creative
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
    log_entry = "Enter your prompt (type 'xxx' to submit or 'exit' to quit): "
    log_and_print(log_entry, color=Fore.GREEN)

def display_spinner(stop_event):
    spinner = ['-', '\\', '|', '/']
    start_time = time.time()
    while not stop_event.is_set():
        for s in spinner:
            elapsed_time = time.time() - start_time
            sys.stdout.write(Fore.BLUE + '\rWaiting for response... {} (Time elapsed: {:.2f} seconds)'.format(s, elapsed_time) + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.2)

    log_entry = f"Waiting for response completed (Total time elapsed: {elapsed_time:.2f} seconds)"
    logging.info(log_entry)

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

    print("")  # Add a newline character before starting the spinner thread
    spinner_thread.start()

    try:
        response = send_to_gpt4(prompt)
    except Exception as e:
        error_message = f"Error: {e}"
        logging.error(error_message)
        print(Fore.RED + f"\n{error_message}" + Style.RESET_ALL)
        response = None
    finally:
        stop_event.set()
        spinner_thread.join()
        sys.stdout.write('\r')
        sys.stdout.flush()

    print("")  # Add a newline character after the spinner thread has finished
    return response

def display_response(response):
    if response:
        log_entry = f"GPT-4 Response:"
        log_and_print(log_entry, color=Fore.CYAN)

        log_entry = f"{response}"
        log_and_print(log_entry, color=Fore.WHITE)

def start_input_loop():
    while True:
        try:
            prompt = get_user_input()
            response = get_gpt4_response(prompt)
            display_response(response)
        except ExitException:
            log_message = "Exiting the program."
            log_and_print(log_message, color=Fore.YELLOW)
            break
        except KeyboardInterrupt:
            log_message = "Detected keyboard interrupt. Exiting the program."
            log_and_print(log_message, color=Fore.YELLOW)
            break
        except Exception as e:
            log_message = f"An unexpected error occurred: {e}"
            log_and_print(log_message, log_type="exception", color=Fore.RED)

if __name__ == '__main__':
    setup_logger()
    clear_screen()
    
    API_KEY = os.environ.get('GPT4_API_KEY')
    if not API_KEY:
        log_entry = f"Error: API key not found in environment variables"
        log_and_print(log_entry, log_type="error", color=Fore.RED)
        sys.exit()    

    start_input_loop()