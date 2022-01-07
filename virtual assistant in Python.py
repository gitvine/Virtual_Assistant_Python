
import speech_recognition as sp
import wikipedia
import pyttsx3
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import threading
import time
from urllib.request import urlopen
import json
import requests
import pywhatkit
import yagmail


class lights():
    # Class to create lights objects
    def __init__(self):
        self.light_status = False

    # method to switch ON lights
    def switch_on(self):
        self.light_status = True

    # method to switch OFF lights
    def switch_off(self):
        self.light_status = False

    # method to get lights status
    def get_status(self):
        return self.light_status


class Email():
    # class to create email object
    def __init__(self):
        self.contacts = {'abcd': 'abcd@gmail.com'}
        self.message = ""
        self.email_flag = False
        self.receiver = ""

    # Setters and getters
    def add_contact(self, contact_name, contact_mail):
        self.contacts[contact_name] = contact_mail

    def get_contacts(self):
        return self.contacts

    def set_message(self, message):
        self.message = message

    def set_receiver(self, receiver):
        self.receiver = receiver

    def set_flag(self):
        self.email_flag = True

    def unset_flag(self):
        self.email_flag = False

    def get_receiver(self):
        return self.receiver

    def get_message(self):
        return self.message

    def get_flag(self):
        return self.email_flag

    def send_mail(self, receiver, message):
        # method to send email
        sender = yagmail.SMTP('abcd@gmail.com', 'xxxxxx')
        sender.send(to=receiver, subject='This is an automated mail', contents=message)


def decode_speech_google(source):
    # Using Google web speech to convert speech to text
    rec = sp.Recognizer()
    print("I am listening!")

    try:
        rec.adjust_for_ambient_noise(source)  # adjusting for noise
        audio = rec.listen(source)  # listening to mic
        detected = rec.recognize_google(audio)  # retrieving the detected text from speech
        print(detected)
        # converting detected string into a list of words
        transcript = detected.strip().upper().split()
        # returning the list
        return transcript
    except:
        # if some error occurs then return the word 'error'
        print("An exception occurred")
        return "error"


def search_command(transcript):
    # Function to search for commands inside the text converted from speech
    command_found = False  # flag to check if any command is found or not
    all_commands = ['WIKIPEDIA', 'LIGHTS', 'WEATHER', 'ACTIVITY', 'PLAY', 'EMAIL', 'GOOGLE', 'TIME',
                    'CHROME']  # List of commands
    for command in all_commands:  # Searching for all the commands through a loop
        if command in transcript:
            print('command found:', command)  # if command is found print 'command found'
            command_found = True  # Set flag to true if command is found
            break;  # break the loop as command has been found

    # We need to call relevant function based on command found
    if (command_found):
        if (command == 'LIGHTS'):
            lights_task(transcript)  # Call function to switch on or off the lights
        elif (command == 'WEATHER'):
            weather()  # Call function to get weather updates
        elif (command == 'ACTIVITY'):
            activity()  # Call function to get activity suggestion
        elif (command == 'WIKIPEDIA'):
            search_wiki(transcript)  # Call function to search information on Wikipedia
        elif (command == 'PLAY'):
            play_song(transcript)
        elif (command == 'EMAIL'):
            ask_message(transcript)
        elif (command == 'GOOGLE'):
            search(transcript)
        elif (command == "TIME"):
            tell_time()
        elif (command == "CHROME"):
            pass;
        else:
            print("I don't know that")  # if no match found, default action
    else:
        print("I don't know that")  # if no match found, default action


def lights_task(transcript):
    # Funtion to switch on or off lights based on command
    # If command ON is found in text then turn ON the lights
    if "ON" in transcript:
        # getting status by calling get status method from lights class
        if (light.get_status()):
            speak('Lights are already ON')
        else:
            light.switch_on()  # calling switch ON method from lights class
            speak('Lights have been turned ON')
    elif "OFF" in transcript:  # If command OFF is found in text then turn OFF lights
        light.switch_off()  # calling switch OFF method from lights class
        speak('Lights have been turned OFF')
    else:  # Default action if ON or OFF couldn't be detected
        if (light.get_status()):
            speak('Lights are currently ON ')
        else:
            speak('Lights are currently OFF')


def activity():
    # Function to connect to an API which suggests an activity
    act = requests.get("https://www.boredapi.com/api/activity/")
    act = act.json()
    print(act['activity'])
    speak(act['activity'])


def play_song(transcript):
    # Function to play video on youtube
    try:
        song = ' '.join(map(str, transcript))
        # Replacing extra words
        song = song.replace('ASSISTANT', '')
        song = song.replace('PLAY', '')
        print('playing ', song)
        speak('playing ' + song)
        pywhatkit.playonyt(song)
    except:
        print('Could not find your request')


def weather():
    city = get_city()
    get_weather(city)


def get_city():
    # opening the URL to get location
    with urlopen("https://geolocation-db.com/jsonp/IP") as url:
        # reading and decoding the URL and storing to Location
        Location = url.read().decode()
        # splitting string with and removing " characters
        Location = Location.split("(")[1].strip(")")
        # converting json to python
        Location = json.loads(Location)
        print(Location['city'])
    return Location['city']


# creating weather function
def get_weather(City_Name):
    # getting data from the URL
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?q=' + City_Name + 'xxxxxxxx')
    # using the content of the request
    A = r.json()
    weather_report = ''
    weather_report += (
                'Current Temperature is ' + str(round(float(A['main']['temp']) - 273.15, 3)) + ' degree celsius ')
    weather_report += ('It feels like ' + str(round(float(A['main']['feels_like']) - 273.15, 3)) + ' degree celsius ')
    weather_report += (
                'Minimum Temperature is ' + str(round(float(A['main']['temp_min']) - 273.15, 3)) + ' degree celsius ')
    weather_report += (
                'Maximum Temperature is ' + str(round(float(A['main']['temp_max']) - 273.15, 3)) + ' degree celsius ')
    print(weather_report)
    speak(weather_report)


def search_wiki(transcript):
    # pip install wikipedia
    # creating a sentence from the list of detected words
    search_string = ' '.join(map(str, transcript))
    # Words to be removed from string before sending for wikipedia search
    extra_word = ['ASSISTANT ', ' SEARCH ', ' ASK ', ' WIKIPEDIA ', ' FOR ', ' ABOUT ']
    for word in extra_word:
        # replacing extra words by blanks
        search_string = search_string.replace(word, ' ')
    print(search_string)
    # getting results from wikipedia API
    try:
        result = wikipedia.summary(search_string, sentences=1)
        # speaking the results
        speak(result)
    except wikipedia.DisambiguationError as e:
        options = e.options[0:5]
        speak('Please be more specific about what you want to search. I got many results like')
        speak(' '.join(map(str, options)))

def list_to_string(list):
    # function to convert list to string
    str = ""
    for element in list:
        str += element + " "
    return str



def ask_message(transcript):
    # function to ask user for message
    search_string = ' '.join(map(str, transcript))
    # removing extra words
    email.receiver = search_string.rstrip().replace('ASSISTANT SEND EMAIL TO ', '')
    print(email.receiver)
    speak('What message would you like to send')
    # Setting email flag to true indicating there is an email to send
    email.email_flag = True


def send_email():
    # function to send email
    contacts = email.get_contacts()
    contact = email.get_receiver()
    message = email.get_message()
    # Checking existence of contact in contact list
    if contact in contacts:
        # getting email id from contact name
        receiver = contacts[contact]
        email.send_mail(receiver, message)
        speak('Your message has been sent')
    else:
        speak('Contact does not exist in your contact list')
    # Unsetting the email details
    email.unset_flag()
    email.set_receiver('')
    email.set_message('')


def speak(audio):
    # Function to convert text into speach
    print(audio)
    # creating an instance of engine
    tts = pyttsx3.init()
    # get the current value of engine
    sound = tts.getProperty('voices')

    # selecting the male voice in property
    tts.setProperty('voice', sound[0].id)
    # Selecting method for speaking
    tts.startLoop(False)
    # Calling function to speak words
    tts.say(audio)
    tts.iterate()
    while tts.isBusy():  # wait until speaking
        time.sleep(0.1)
    tts.endLoop()  # Ending the loop


# obtain audio from the microphone


def start_assistant():
    global awake_flag  # Flag to check if wake word is detected
    global light_status  # Flag to check the current status of lights
    light_status = 0  # Initially lights are OFF
    awake_flag = False  # Initially assistant is not awake
    with sp.Microphone() as source:
        while 1:
            print("decoding")
            transcript = decode_speech_google(source)  # calling function to decode the speech
            if (transcript != 'error'):  # check if error is returned from decoder

                if (transcript is not NONE and transcript[0] == 'ASSISTANT'):  # check if wake word is detected
                    panel.configure(image=img2)  # changing mic image to green if wake word is detected
                    panel.image = img2  # updating te image
                    print("Wake word detected!")
                    speak("Hi!")  # Speak Hi
                    awake_flag = True  # setting wake flag to true
                    search_command(transcript)  # Search for the command in the decoded transcript
                    # Action has now been performed
                    panel.configure(image=img)  # Again change mic image to inactive
                    panel.image = img
                    awake_flag = False  # awake flag is disabled
                elif (email.get_flag()):
                    email.set_message(transcript)
                    send_email()
                # if (awake_flag):
                # stopping after first wake word, will change this later to implement continuous monitoring
                #    print("I am stopping after first first wake word detection as I am tired.")
                #    break


light = lights()  # Creating a light object
email = Email()     # Creating an email object
window = tk.Tk()  # creating an instance of tinker window
window.title("Assistant")  # Providing title for window
window.geometry("600x600")  # Providing shape for window
window.configure(background='white')  # Providing background colour

path = "mic.jpg"  # Path to Inactive mic image
path2 = "mic2.jpg"  # Path to active mic image

# Creating the images to be used to display in window
img = ImageTk.PhotoImage(Image.open(path))
img2 = ImageTk.PhotoImage(Image.open(path2))
# Creating panel and showing inactive mic image
panel = tk.Label(window, image=img)
# Placing mic at bottom location using pack
panel.pack(side="bottom", fill="both", expand="yes")
# Creating a label with assistant information and starting the assistant thread
b1 = Label(window, text='Hi! I am your virtual assistant. Try asking me things like :\n'
                        ' "Assistant Search Wikipedia for Western University","Assistant play Jingle Bells" \n '
                        '"Assistant Switch On the lights" "Assistant give me weather updates"',
           command=threading.Thread(target=start_assistant).start())
# placing label on the window
b1.pack(pady=10)
# Starting the loop for tkinter GUI
window.mainloop()
