import sys
import openai
import threading
from modules.output import display_spinner
from modules.custom_logger import CustomLogger
from modules.message_history import MessageHistory

logger = CustomLogger("gpt4_shell") # get ref to singleton logger

def wait_for_query_show_spinner(prompt, api_key):
    # Query GPT-4 and show a spinner while waiting for the response
    console = logger.console

    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=display_spinner, args=(stop_event,))
    spinner_thread.daemon = True

    response = query_gpt(prompt, api_key)
    
    console.print("")  # blank line before spinner
    spinner_thread.start()

    try:
        stop_event.set()
        spinner_thread.join()
        console.print("\r", end="")
        sys.stdout.flush()
    finally:
        console.print("")  # blank line after spinner

    return response


message_history = MessageHistory()  
def query_gpt(text, api_key):
    # Query GPT-4 with the given text and api_key
    openai.api_key = api_key

    # Add the user's message to the history
    message_history.add_message("user", text)

    # Calculate available tokens for AI's message
    available_tokens = message_history.max_tokens - message_history.current_tokens

    # Log and print the current message length in tokens
    log_entry = f"Current message token length: {message_history.current_tokens}"
    logger.log_and_print(log_entry, style="magenta") # use magenta color for pink text

    # Actual query
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message_history.get_history(),
        max_tokens=available_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )

    if response.choices:
        message = response['choices'][0]['message']['content'].strip()
        # Add AI's response to the history
        message_history.add_message("assistant", message)
        return message

    return "I'm not sure how to respond to that."