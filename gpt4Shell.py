import openai
import threading
import os
import sys
import time
from colorama import Fore, Style

<<<<<<< HEAD
API_KEY = os.environ.get('GPT4_API_KEY')
if not API_KEY:
    print(Fore.RED + f"\nError: API key not found in environment variables" + Style.RESET_ALL)
    sys.exit()

class ExitException(Exception):
    pass
=======
# Add your GPT-4 API key here
API_KEY = ""
>>>>>>> b795d90acfe6fe953ff4d7c321a5be69b8d367b1

def send_to_gpt4(text):
    openai.api_key = API_KEY

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=7000,    # 8k max
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
    print(Fore.GREEN + "\nEnter your prompt (type '///' to submit or 'exit' to quit): " + Style.RESET_ALL)

def display_spinner(stop_event):
    spinner = ['-', '\\', '|', '/']
    start_time = time.time()
    while not stop_event.is_set():
        for s in spinner:
            elapsed_time = time.time() - start_time
            sys.stdout.write(Fore.BLUE + '\rWaiting for response... {} (Time elapsed: {:.2f} seconds)'.format(s, elapsed_time) + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.2)

def clear_screen():
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for Linux and macOS
        os.system('clear')

def get_user_input():
    display_instructions()
    return read_input()

def get_gpt4_response(prompt):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=display_spinner, args=(stop_event,))
    spinner_thread.daemon = True

    print("")  # Add a newline character before starting the spinner thread
    spinner_thread.start()

    try:
        response = send_to_gpt4(prompt)
    except Exception as e:
        print(Fore.RED + f"\nError: {e}" + Style.RESET_ALL)
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
        print(Fore.CYAN + "\nGPT-4 Response:" + Style.RESET_ALL)
        print(Fore.WHITE + "{}".format(response) + Style.RESET_ALL)

def start_input_loop():
    clear_screen()
    
    while True:
        try:
            prompt = get_user_input()

            response = get_gpt4_response(prompt)

            display_response(response)
        except ExitException:
            print(Fore.YELLOW + "\nExiting the program." + Style.RESET_ALL)
            break
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nDetected keyboard interrupt. Exiting the program." + Style.RESET_ALL)
            break

if __name__ == '__main__':
<<<<<<< HEAD
    start_input_loop()
=======
    startInputLoop()
>>>>>>> b795d90acfe6fe953ff4d7c321a5be69b8d367b1
