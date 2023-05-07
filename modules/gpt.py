import sys
import openai
import threading
from modules.output import display_spinner
from modules.custom_logger import CustomLogger

logger = CustomLogger("gpt4_shell") # get ref to singleton logger

def get_gpt4_response(prompt, api_key):
    console = logger.console  # Access the console object from the logger
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=display_spinner, args=(stop_event,))
    spinner_thread.daemon = True

    console.print("")  # Add a newline character before starting the spinner thread
    spinner_thread.start()

    try:
        response = send_to_gpt4(prompt, api_key)
    except Exception as e:
        error_message = f"Error: {e}"
        logger.log_and_print(error_message, log_type="error")
        response = None
    finally:
        stop_event.set()
        spinner_thread.join()
        console.print("\r", end="")
        sys.stdout.flush()

    console.print("")  # Add a newline character after the spinner thread has finished
    return response

def send_to_gpt4(text, api_key):
    openai.api_key = api_key

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