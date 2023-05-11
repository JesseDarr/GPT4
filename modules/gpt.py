import sys
import openai
import threading
from modules.output import display_spinner
from modules.custom_logger import CustomLogger
from modules.message_history import MessageHistory

message_history = MessageHistory()
logger = CustomLogger("gpt4_shell")  # get reference to singleton logger

def wait_for_query_show_spinner(prompt, api_key):
    # Orchestrate the process of querying GPT-4 and show a spinner while waiting for the response.
    available_tokens = prepare_query(prompt)
    stop_event = threading.Event()
    spinner_thread = create_spinner_thread(stop_event)
    start_spinner_thread(spinner_thread)
    response = query_gpt(api_key, available_tokens)
    stop_spinner_thread(stop_event, spinner_thread)
    return response

def prepare_query(prompt):
    # Prepare a query to GPT-4, add the user's message to the history and calculate available tokens.
    add_user_message_to_history(prompt)
    available_tokens = calculate_available_tokens()
    log_current_message_length()
    return available_tokens

def add_user_message_to_history(prompt):
    # Add the user's message to the conversation history.
    message_history.add_message("user", prompt)

def calculate_available_tokens():
    # Calculate the number of tokens available for the AI's message.
    return message_history.max_tokens - message_history.current_tokens

def log_current_message_length():
    # Log and print the current message length in tokens.
    log_entry = f"Current message token length: {message_history.current_tokens}"
    logger.log_and_print(log_entry, style="magenta")

def create_spinner_thread(stop_event):
    # Create a new spinner thread.
    spinner_thread = threading.Thread(target=display_spinner, args=(stop_event,))
    spinner_thread.daemon = True
    return spinner_thread

def start_spinner_thread(spinner_thread):
    # Start the spinner thread.
    logger.console.print("")  # blank line before spinner
    spinner_thread.start()

def stop_spinner_thread(stop_event, spinner_thread):
    # Stop the spinner thread and clean up the output.
    stop_event.set()
    spinner_thread.join()
    logger.console.print("\r", end="")
    sys.stdout.flush()
    logger.console.print("")  # blank line after spinner

def query_gpt(api_key, available_tokens):
    # Query GPT-4 and process the response.
    openai.api_key = api_key
    response = create_chat_completion(api_key, available_tokens)
    return process_chat_completion_response(response)

def create_chat_completion(api_key, available_tokens):
    # Create a chat completion request to GPT-4.
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=message_history.get_history(),
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )

def process_chat_completion_response(response):
    # Process the response from GPT-4, returning the message or a default string.
    if response.choices:
        message = response['choices'][0]['message']['content'].strip()
        message_history.add_message("assistant", message)
        return message
    return "I'm not sure how to respond to that."