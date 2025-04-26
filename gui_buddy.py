import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pywhatkit
import pyautogui
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
import speech_recognition as sr

# Initialize pyttsx3
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 6:
        greeting = "Hey Owl!"
    elif hour >= 6 and hour < 12:
        greeting = "Good Morning!"
    elif hour >= 12 and hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    speak(greeting)
    speak("I am Buddy, your assistant. How may I help you today?")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
    except Exception:
        speak("Sorry, could you say that again?")
        return "None"
    return query.lower()


# Functionalities
def search_wikipedia():
    query = take_command()
    if query:
        speak("Searching Wikipedia...")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        messagebox.showinfo("Wikipedia Result", results)


def open_website(url, site_name):
    webbrowser.open(url)
    speak(f"Opening {site_name}")


def play_music(directory):
    try:
        songs = os.listdir(directory)
        os.startfile(os.path.join(directory, songs[0]))
        speak("Playing music")
    except Exception:
        speak("Could not find the music directory")


def tell_time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {time}")


def my_location():
    geolocator = Nominatim(user_agent="myGeocoder")
    g = geocoder.ip('me')
    location = g.latlng
    speak(f"Your current location is approximately latitude {location[0]} and longitude {location[1]}")


def send_email():
    try:
        speak("What should I say?")
        content = take_command()
        to = "recipient@example.com"  # Replace with recipient email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_password")
        server.sendmail("your_email@gmail.com", to, content)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        speak(f"Sorry, I could not send the email. {e}")


# GUI Setup
def create_gui():
    # Main Window
    root = tk.Tk()
    root.title("Buddy Assistant")
    root.geometry("800x600")
    root.configure(bg="#1e1e1e")  # Dark theme background

    # Header
    header = tk.Label(root, text="Buddy Assistant", font=("Helvetica", 24, "bold"), fg="white", bg="#1e1e1e")
    header.pack(pady=20)

    # Add Image
    img = Image.open("assistant.png")  # Add your image in the project directory
    img = img.resize((150, 150), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=photo, bg="#1e1e1e")
    img_label.pack()

    # Buttons
    button_frame = tk.Frame(root, bg="#1e1e1e")
    button_frame.pack(pady=20)

    buttons = [
        ("Search Wikipedia", search_wikipedia),
        ("Open YouTube", lambda: open_website("https://www.youtube.com", "YouTube")),
        ("Open Google", lambda: open_website("https://www.google.com", "Google")),
        ("Play Music", lambda: play_music("G:\\gui buddyyyyy\\music")),
        ("Play Favorite Song", lambda: play_music("G:\\gui buddyyyyy\\loved music")),
        ("Tell Time", tell_time),
        ("My Location", my_location),
        ("Send Email", send_email),
    ]

    for text, command in buttons:
        btn = tk.Button(
            button_frame, text=text, font=("Helvetica", 12), width=20, bg="#282828", fg="white", command=command
        )
        btn.pack(pady=10)

    # Start the app
    root.after(1000, wish_user)
    root.mainloop()
    
def handler(request):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "Hello from Python on Vercel!"
    }


if __name__ == "__main__":
    create_gui()
