import speech_recognition as sr
import pyttsx3
import openai

# https://gist.github.com/Daniel-V-Richardson/a009bac48efd55db4887a05eaffa836b

# Set OpenAI API Key
openai.api_key = "Your API Key"

# Initialize and set properties for text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

# Initialize recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

# Define names for user and bot, and an empty string for the conversation
conversation = ""
user_name = "Dan"
bot_name = "John"

# Main body of the chatbot
while True:
    # Listen to microphone input
    with mic as source:
        print("\n Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("no longer listening")

    # Transcribe audio input to text using Google's speech recognition service
    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    # Check for exit phrase
    if "quit" in user_input.lower() or "exit" in user_input.lower():
        print("Exiting chatbot...")
        break

    # Create the prompt string
    prompt = user_name+":"+user_input + "\n"+bot_name+":"
    conversation += prompt

    # Use OpenAI API to generate response to prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=conversation,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract response from API and add to conversation
    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(
        user_name + ":", 1)[0].split(bot_name + ":", 1)[0]

    conversation += response_str + "\n"
    print(response_str)

    # Pass response to text-to-speech engine to be spoken
    engine.say(response_str)
    engine.runAndWait()
