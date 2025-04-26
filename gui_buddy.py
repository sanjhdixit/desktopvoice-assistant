import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import speech_recognition as sr
from geopy.geocoders import Nominatim
import geocoder
import re
import pyautogui  # Library to simulate keyboard/mouse actions
import requests

# Initialize pyttsx3
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine_lock = threading.Lock()

def speak(audio):
    with engine_lock:
        engine.say(audio)
        engine.runAndWait()

def wish_user():
    hour = int(datetime.datetime.now().hour)
    greeting = "Good Morning!" if 6 <= hour < 12 else "Good Afternoon!" if 12 <= hour < 18 else "Good Evening!" if hour >= 18 else "Hey Owl!"
    speak(greeting)
    speak("I am Buddy, your assistant. How may I help you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return "none"
    except sr.RequestError:
        speak("I am having trouble connecting to the speech recognition service.")
        return "none"

def match_command(query, commands):
    for command in commands:
        if re.search(command, query, re.IGNORECASE):
            return command
    return None

def search_wikipedia():
    speak("What should I search on Wikipedia?")
    query = take_command()
    if query != "none":
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
            messagebox.showinfo("Wikipedia Result", results)
        except Exception as e:
            speak("I couldn't find any results. Please try a different query.")

def search_on_google():
    speak("What should I search on Google?")
    query = take_command()
    if query != "none":
        speak(f"Searching for {query} on Google")
        webbrowser.open(f"https://www.google.com/search?q={query}")

def search_on_youtube():
    speak("What should I search on YouTube?")
    query = take_command()
    if query != "none":
        speak(f"Searching for {query} on YouTube")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def play_music(directory):
    try:
        songs = os.listdir(directory)
        if songs:
            os.startfile(os.path.join(directory, songs[0]))
            speak("Playing music")
        else:
            speak("No music found in the directory.")
    except Exception as e:
        speak(f"Error playing music: {e}")

def tell_time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {time}")

def my_location():
    try:
        geolocator = Nominatim(user_agent="myGeocoder")
        g = geocoder.ip('me')
        location = g.latlng
        if location:
            speak(f"Your current location is approximately latitude {location[0]} and longitude {location[1]}")
        else:
            speak("Sorry, I couldn't fetch your location.")
    except Exception as e:
        speak(f"An error occurred while fetching location. {e}")

def send_email():
    try:
        speak("What should I say?")
        content = take_command()
        if content != "none":
            to = "sonishreyyaa786@gmail.com"
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("sanjhdixit1@gmail.com", "Abcdefgh11")
            server.sendmail("sanjhdixit1@gmail.com", to, content)
            server.close()
            speak("Email has been sent successfully!")
    except Exception as e:
        speak(f"Sorry, I could not send the email. {e}")

def where_is():
    speak("Which place would you like to know about?")
    place = take_command()
    if place != "none":
        webbrowser.open(f"https://www.google.com/maps/search/{place}")
        speak(f"Searching for {place} on Google Maps.")

def open_whatsapp():
    speak("Opening WhatsApp.")
    webbrowser.open("https://web.whatsapp.com/")

def open_website(url, site_name):
    webbrowser.open(url)
    speak(f"Opening {site_name}")

def open_netflix():
    webbrowser.open("https://www.netflix.com")
    speak("Opening Netflix for you")

# Functions to control YouTube video
def play_video():
    pyautogui.press('k')  # Play in YouTube
    speak("Playing or Pausing the video.")

def pause_video():
    pyautogui.press('k')  # Pause the video
    speak("Pausing the video.")

def skip_video():
    pyautogui.press('l')  # Skip 10 seconds
    speak("Skipping the video.")

def voice_assistant():
    while True:
        query = take_command()
        if query == "none":
            continue
        if match_command(query, ["search wikipedia"]):
            search_wikipedia()
        elif match_command(query, ["search on google", "search google"]):
            search_on_google()
        elif match_command(query, ["search youtube", "search on youtube"]):
            search_on_youtube()
        elif match_command(query, ["open youtube"]):
            open_website("https://www.youtube.com", "YouTube")
        elif match_command(query, ["open google"]):
            open_website("https://www.google.com", "Google")
        elif match_command(query, ["play music"]):
            play_music("G:\\gui buddyyyyy\\music")
        elif match_command(query, ["play favorite song"]):
            play_music("G:\\gui buddyyyyy\\loved music")
        elif match_command(query, ["tell time", "what time"]):
            tell_time()
        elif match_command(query, ["my location", "where am i"]):
            my_location()
        elif match_command(query, ["send email"]):
            send_email()
        elif match_command(query, ["where is", "find location"]):
            where_is()
        elif match_command(query, ["movie time"]):
            open_netflix()
        elif match_command(query, ["open whatsapp"]):
            open_whatsapp()
        elif match_command(query, ["open", "open website"]):
            speak("Which website would you like to open?")
            website_name = take_command()
            if website_name != "none":
                open_website(f"https://{website_name}.com", website_name)
        elif match_command(query, ["pause video", "pause youtube"]):
            pause_video()
        elif match_command(query, ["play video", "play youtube"]):
            play_video()
        elif match_command(query, ["skip video", "skip youtube"]):
            skip_video()
        elif match_command(query, ["exit", "quit"]):
            speak("Goodbye!")
            break

def create_gui():
    root = tk.Tk()
    root.title("Buddy Assistant")
    root.geometry("800x600")
    root.configure(bg="#1e1e1e")

    header = tk.Label(root, text="Buddy Assistant", font=("Helvetica", 24, "bold"), fg="white", bg="#1e1e1e")
    header.pack(pady=20)

    img = Image.open("assistant.png")
    img = img.resize((150, 150), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=photo, bg="#1e1e1e")
    img_label.pack()

    button_frame = tk.Frame(root, bg="#1e1e1e")
    button_frame.pack(pady=20)

    buttons = [
        ("Search Wikipedia", search_wikipedia),
        ("Search on Google", search_on_google),
        ("Search on YouTube", search_on_youtube),
        ("Play Music", lambda: play_music("G:\\gui buddyyyyy\\music")),
        ("Play Favorite Song", lambda: play_music("G:\\gui buddyyyyy\\loved music")),
        ("Tell Time", tell_time),
        ("My Location", my_location),
        ("Send Email", send_email),
        ("Where is", where_is),
        ("Movie Time", open_netflix),
        ("Open WhatsApp", open_whatsapp),
        ("Play/Pause Video", play_video),
        ("Skip Video", skip_video),
        ("Pause Video", pause_video),
    ]

    for text, command in buttons:
        btn = tk.Button(button_frame, text=text, font=("Helvetica", 12), width=20, bg="#282828", fg="white", command=command)
        btn.pack(pady=10)

    threading.Thread(target=voice_assistant, daemon=True).start()
    root.after(1000, wish_user)
    root.mainloop()

if __name__ == "__main__":
    create_gui()

