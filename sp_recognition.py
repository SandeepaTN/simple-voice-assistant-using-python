import speech_recognition as sr
import webbrowser
import requests
import json
import random
from pytube import YouTube
import pyttsx3
import pyjokes

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define a function for voice commands
def voice_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            # Recognize speech using Google Speech Recognition
            command = r.recognize_google(audio)
            print("You said:", command)
            
            # Process the command
            process_command(command)
            
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand you.")
        except sr.RequestError:
            print("Sorry, I'm unable to process your request.")

# Define a function to process the voice command
try:
    def process_command(command):
        if "hello" in command:
            print("Hello there!")
            speak_text("Hello there!")
        elif "goodbye" in command:
            print("Goodbye!")
            speak_text("Goodbye!")
        elif "play" in command or "YouTube" in command:
            print("Playing video...")
            speak_text("Playing video...")
            play_video(command)
        elif "search" in command:
            search_wikipedia(command)
        elif "joke" in command:
            tell_joke()
        elif "what is your name" in command:
            speak_text("my name is  sandy")   
        else:
            print("Command not recognized.")
            speak_text("Command not recognized.")

    # Define a function to play a video from YouTube
    def play_video(command):
        # Extract the search query from the command
        search_query = command.replace("play", "").replace("YouTube", "").strip()

        # Search for the video on YouTube
        url = f"https://www.youtube.com/results?search_query={search_query}"
        response = requests.get(url).text

        # Find the first video in the search results
        start_index = response.index('watch?v=')
        end_index = response.index('"', start_index)
        video_id = response[start_index:end_index]
        video_url = f"https://www.youtube.com/{video_id}"

        # Play the video
        webbrowser.open(video_url)



    # Define a function to perform a Wikipedia search and read the summary

    def search_wikipedia(command):
        search_term = command.replace("search", "").strip()
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={search_term}"
        response = requests.get(url).json()
        
        if 'query' in response and 'pages' in response['query']:
            pages = response['query']['pages']
            page_id = list(pages.keys())[0]
            
            if page_id != '-1':
                page_data = pages[page_id]
                page_summary = page_data['extract']
                print("Wikipedia summary:")
                print(page_summary)
                speak_text(page_summary)
                page_title = page_data['title']
                page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
                webbrowser.open(page_url)
                print("Opening Wikipedia page for", page_title)
            else:
                print("No Wikipedia results found.")
                speak_text("No Wikipedia results found.")
        else:
            print("Error occurred while searching Wikipedia.")
            speak_text("Error occurred while searching Wikipedia.")

    # Define a function to tell a joke
    def tell_joke():
        joke = pyjokes.get_joke()
        print("Here's a joke for you:")
        print(joke)
        speak_text("Here's a joke for you:")
        speak_text(joke)

    # Define a function to convert text to speech
    def speak_text(text):
        engine.say(text)
        engine.runAndWait()

    # Run the voice command function in a loop
    while True:
        voice_command()
except:
    print("Result not found")