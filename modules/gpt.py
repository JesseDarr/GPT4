import sys
import openai
import threading
from modules.output import display_spinner
from modules.utils import MessageHistory
from modules.custom_logger import CustomLogger

logger = CustomLogger("gpt4_shell") # get ref to singleton logger

def wait_for_query_show_spinner(prompt, api_key):
    # Query GPT-4 and show a spinner while waiting for the response
    console = logger.console

    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=display_spinner, args=(stop_event,))
    spinner_thread.daemon = True

    console.print("")  # blank line after spinner stops
    spinner_thread.start()

    try:
        response = query_gpt(prompt, api_key)
    finally:
        stop_event.set()
        spinner_thread.join()
        console.print("\r", end="")
        sys.stdout.flush()

    console.print("")  # blank line after spinner stops
    return response

message_history = MessageHistory()  
def query_gpt(text, api_key):
    # Query GPT-4 with the given text and api_key
    openai.api_key = api_key

   # Add the user's message to the history
    message_history.add_message("user", text)

    # Actual query
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message_history.get_history(),
        max_tokens=6500,
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