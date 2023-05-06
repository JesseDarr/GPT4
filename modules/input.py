import logging

def get_user_input():
    display_instructions()
    user_input = read_input()
    log_entry = f"User Input: {user_input}"
    logging.info(log_entry)
    return user_input

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