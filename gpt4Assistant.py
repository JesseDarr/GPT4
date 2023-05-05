import speech_recognition as sr
import openai
import pyttsx3

# Add your GPT-4 API key here
API_KEY = ""

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
        temperature=0.5,
    )

    if response.choices:
        message = response['choices'][0]['message']['content'].strip()
        return message

    return "I'm not sure how to respond to that."

def text_to_speech(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"\nException: {e}")

def speech_to_text():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            while True:
                print("\nSpeak now...")

                audio = r.listen(source)

                try:
                    text = r.recognize_google(audio)
                    print("\nYou said: {}".format(text))

                    if "close program" in text:
                        break

                    response = send_to_gpt4(text)
                    print("\nGPT-4 Response: {}".format(response))
                    text_to_speech(response)

                except sr.UnknownValueError:
                    print("\nSorry, I didn't catch that.")
                except sr.RequestError:
                    print("\nSorry, I'm having trouble accessing the speech recognition service.")

    except OSError:
            print("\nNo default input device (microphone) is available. Please connect a microphone and try again.")

if __name__ == '__main__':
    speech_to_text()