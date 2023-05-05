import openai

# Add your GPT-4 API key here
API_KEY = "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"

def send_to_gpt4(text):
    openai.api_key = API_KEY

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=8000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    if response.choices:
        message = response['choices'][0]['message']['content'].strip()
        return message

    return "I'm not sure how to respond to that."

def startInputLoop():
    while True:
        prompt = input("\nEnter your prompt (or type 'exit' to quit): ")

        if prompt == 'exit':
            break

        response = send_to_gpt4(prompt)
        print("\nGPT-4 Response: {}".format(response))

if __name__ == '__main__':
    startInputLoop()