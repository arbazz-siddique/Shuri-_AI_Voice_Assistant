import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import pywhatkit
import os
import time
import pyautogui  # For WhatsApp message automation
import googlemaps
import pyaudio
import random

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Initialize Google Maps client (replace 'YOUR_API_KEY' with your actual Google Cloud API key)
gmaps = googlemaps.Client(key='AIzaSyDYRqh3Y2pvZcTd_0dM95T7tkzrGZl0VHI')

def speak(audio):
    """Speak the given text."""
    engine.say(audio)
    engine.runAndWait()

def take_command():
    """Take voice input and return as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception:
        print("Could you say that again?")
        return "None"
    return query.lower()

def send_whatsapp_message():
    """Send a WhatsApp message after confirming the correct contact."""

    speak("Who do you want to send a message to?")
    
    while True:
        contact_name = take_command().lower()
        
        if contact_name == "none":  
            speak("I couldn't recognize the name. Please say that again.")
        else:

            break  # Exit loop when a valid name is provided

    speak(f"Searching for {contact_name} in WhatsApp.")
    os.system("start whatsapp:")  # Open WhatsApp Desktop
    time.sleep(5)  # Allow WhatsApp to load

    # Open search box
    pyautogui.hotkey('ctrl', 'f')  # Open search
    time.sleep(1)
    pyautogui.write(contact_name)  # Type contact name
    time.sleep(2)

    # Fetch contact list (WhatsApp highlights multiple matches)
    speak("I found multiple contacts. Please say the name of the correct contact.")

    while True:
        selected_contact = take_command()
        if selected_contact == "none":
            speak("I couldn't recognize the selected name. Please try again.")
        else:
            break  # Valid name received

    # Clear search and enter correct contact
    pyautogui.hotkey('ctrl', 'f')  # Reopen search
    time.sleep(1)
    pyautogui.write(selected_contact)  # Type correct contact name
    time.sleep(2)
    pyautogui.press('down')  # Move to the first match
    time.sleep(1)
    pyautogui.press('enter')  # Select contact
    time.sleep(2)

    # Ask for message
    speak(f"What message should I send to {selected_contact}?")

    while True:
        message = take_command()
        if message == "none":
            speak("I couldn't recognize the message. Please say that again.")
        else:
            break  # Valid message received

    # Type and send the message
    pyautogui.write(message)
    time.sleep(1)
    pyautogui.press('enter')  # Send the message

    speak(f"Message sent to {selected_contact}.")


def get_directions_and_distance(destination):
    """Fetches directions and distance to the destination."""
    try:
        current_location = "Your City or Current Location"  # Replace with actual location
        directions_result = gmaps.directions(
            origin=current_location,
            destination=destination,
            mode="driving"
        )
        distance = directions_result[0]['legs'][0]['distance']['text']
        duration = directions_result[0]['legs'][0]['duration']['text']

        speak(f"The destination is {distance} away and it will take approximately {duration} to reach by car.")
        print(f"Distance: {distance}, Duration: {duration}")
        webbrowser.open(f"https://www.google.com/maps/dir/{current_location}/{destination}")
    except Exception as e:
        speak("Sorry, I could not fetch directions at the moment.")
        print(f"Error: {e}")

def main(first_time=True):
    """Main function to handle user commands."""
    if first_time:
        hour = int(datetime.datetime.now().hour)
        if hour < 12:
            speak("Good morning, sir.")
        elif hour < 18:
            speak("Good afternoon, sir.")
        else:
            speak("Good evening, sir.")
        speak("I am Shuri, how may I help you?")

    while True:
        query = take_command()

        # Wikipedia search
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError:
                speak("The query is ambiguous, please specify further.")
            except Exception:
                speak("Sorry, I couldn't fetch data from Wikipedia.")

        # Open YouTube
        elif 'open youtube' in query:
            if 'search' in query or 'play' in query:
                search_query = query.replace("open youtube", "").replace("search", "").replace("play", "").strip()
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
                pywhatkit.playonyt(search_query)
                speak(f"I found these results on YouTube for {search_query}.")
            else:
                webbrowser.open("https://www.youtube.com")
                speak("Opening YouTube.")

        # Google search
        elif 'google search' in query:
            query = query.replace("google search", "").replace("google", "")
            speak("Here is what I found on the web.")
            pywhatkit.search(query)

        # Greeting
        elif "who are you" in query:
            speak("I'm Shuri, your AI assistant.")
        
        elif 'hello' in query:
            speak("Hello, how can I help you, sir?")
        
        elif 'how are you' in query:
            speak("I'm fine, thank you. How about you, sir?")
        
        elif 'i am fine' in query or "i'm fine" in query or "i am good" in query:
            speak("That's great, sir! Let's do something fun.")

        # Time inquiry
        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            speak(f"Sir, the time is {str_time}.")
        
        elif 'thank' in query or 'thank you' in query:
            responses = [

            "You're always welcome, sir! Let me know if there's anything else I can do for you.",
            "My pleasure, sir! Helping you is what I’m here for. Need anything else?",
            "No need to thank me, sir! I'm always at your service. What’s next on the agenda?",
            "I'm honored to assist you, sir! Shall we tackle another task together?",
            "It’s always a delight to help you, sir! Just say the word, and I’m here."
        ]
   
            speak(random.choice(responses))


        # Open VS Code
        elif 'open code' in query:
            code_path = "C:\\Users\\Acer\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            speak("Launching VS Code, sir.")
            os.startfile(code_path)

        # Open Google Maps
        elif 'open map' in query:
            if 'search' in query or 'for' in query:
                map_query = query.replace("open map", "").replace("search", "").replace("for", "").strip()
                get_directions_and_distance(map_query)
            else:
                webbrowser.open("https://www.google.com/maps")
                speak("Opening Google Maps.")

        # Send WhatsApp message
        elif 'send a message' in query or 'whatsapp' in query:
            send_whatsapp_message()

        # Shutdown system
        elif 'shutdown the system' in query:
            speak("Are you sure you want to shut down your system, sir? Please say 'yes' to confirm or 'no' to cancel.")
            confirmation = take_command()
            if 'yes i want' in confirmation:
                speak("Shutting down the system now, sir.")
                os.system("shutdown /s /t 1")
            elif 'no' in confirmation:
                speak("Shutdown cancelled, sir.")
            else:
                speak("I didn't catch that, sir. Please say 'yes' or 'no'.")

        # Exit command
        elif 'you need a break' in query:
            speak("Okay, sir, you can call me anytime by saying 'wake up Shuri.'")
            return  # Exit the main function and wait for "wake up"

if __name__ == '__main__':
    first_time = True
    while True:
        if first_time:
            main(first_time)
            first_time = False
        else:
            print("Listening for 'wake up'...")
            wake_command = take_command()
            if 'wake up' in wake_command:
                main(first_time=False)
