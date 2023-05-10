import nltk

class MessageHistory:
    # Used to track message history to inject back into the queries
    def __init__(self, max_tokens=4000):
        # nltk IS NOT THE SAME tokenizer used by GPT, in order to use that we must have torch
        # to prevent some weird output tokenizer produces when torch isn't installed, even though it's not being used
        # torch breaks the logging completely
        # Given our 4000 token limit, nltk is a clouse enough estimate for our purposes
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer() 
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.history = [
            {"role": "system", "content": "You are a helpful assistant. Be precise, concise, and somewhat informal. Avoid using non-ASCII characters, such as emojis, that may cause encoding issues."},
            {"role": "system", "content": "When providing code, please enclose it in triple backticks with the appropriate language specified."},
        ]
        self.current_tokens += self.count_tokens(self.history)

    def add_message(self, role, content):
        # Adds message to history
        message = {"role": role, "content": content}
        message_tokens = self.count_tokens(message)
        if self.current_tokens + message_tokens > self.max_tokens:
            self.trim_history(self.current_tokens + message_tokens - self.max_tokens)
        self.history.append(message)
        self.current_tokens += message_tokens

    def get_history(self):
        return self.history

    def count_tokens(self, messages):
        if isinstance(messages, dict):
            messages = [messages]
        return sum(len(self.tokenizer.tokenize(msg["content"])) for msg in messages)

    def trim_history(self, tokens_to_remove):
        # Removes oldest message from history until we've removed enough tokens
        tokens_removed = 0
        while tokens_removed < tokens_to_remove:
            removed_message = self.history.pop(0)
            tokens_removed += self.count_tokens(removed_message)
        self.current_tokens -= tokens_removed