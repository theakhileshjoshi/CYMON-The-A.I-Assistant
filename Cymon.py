#import starts froms here
import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
from speech_recognition import Microphone
import wikipedia
import webbrowser
import pyowm
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import os
import subprocess
import random
from covid import Covid
#import ends

engine = pyttsx3.init('sapi5')##Engine defination
voices = engine.getProperty('voices')##Defining voices

engine.setProperty(voices, voices[0].id)##Voice properites

###Function for text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    pass

###function for taking audio command
def takeCommand():
    '''
    input: Voice input from microphone.
    Process: Recognises the string in the voice
    :return: string form of the voice input
    '''
    r = sr.Recognizer()
    with sr.Microphone() as s:
        print("Listening..")
        audio = r.listen(s)
    try:
        print("Recognising..")
        query = r.recognize_google(audio, language="en-in")
    except Exception as e:
        print(e)
        speak("Pardon Sir.")
        return None
    return query

###Function for wish me
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning L")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon L")
    elif hour >= 18 and hour <= 24:
        speak("Good Evening L")
    speak("How can I help you")

###Program starts from here
if __name__ == "__main__":
    speak("Hello L")
    wish_me()
    query = takeCommand().lower()
    print(query)
    ###Program for wikipedia search
    if 'wikipedia' in query:
        speak("Searching all info about it")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        if results == True:
            speak("Sorry I got Nothing.")
        else:
            speak("This is what I found. " + results)
    ###Program to open youtube.com
    elif 'open youtube' in query:
        webbrowser.open("youtube.com")
    ###Program to open google.com
    elif 'open google' in query:
        webbrowser.open("google.com")
    elif 'open facebook' in query:
    ###Program to open facebook.com
        webbrowser.open("facebook.com")
    elif '.com' in query:
    ###Program to open some website
        webbrowser.open(query)
    ###Program to check for commands like weather,news,to do list, 
    elif 'catch' in query:
        speak("On what topic sir ?")
        query = takeCommand().lower()
        if 'weather' in query:
            CITY = 'Pune'
            owm = pyowm.OWM('206301b214c12e0bcc7c1dcc170fb7a6')
            API_KEY = '206301b214c12e0bcc7c1dcc170fb7a6'
            BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
            URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
            response = requests.get(URL)
            if response.status_code == 200:
                # getting data in the json format
                data = response.json()
                # getting the main dict block
                main = data['main']
                # getting temperature
                temperature = main['temp']
                # getting the humidity
                humidity = main['humidity']
                # getting the pressure
                pressure = main['pressure']
                # weather report
                report = data['weather']

                speak("Temperature today is ")
                speak(temperature)
                speak("And Humidity ")
                speak(humidity)
                speak("Pressure Today is ")
                speak(pressure)
                speak("Pascals")
                speak("In short its a " + report[0]['description'])
            else:
                # showing the error message
                speak("I  got nothing")

        if 'news' in query:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()

            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            # Print news title, url and publish date
            for news in news_list:
                speak(news.title.text)
                speak(news.pubDate.text)

        if 'to do list' in query:
            task = []
            print("Tasks are here")
            if len(task) == 0:
                speak('You Dont have any task today.')
                speak('Want to add some task or reset it?')
                ask = takeCommand().lower()
                if 'yes' in ask:
                    speak('What would you like to do.')
                    speak('add')
                    speak('reset')
                    ask = takeCommand().lower()
                    print(ask)
                    if 'add' or 'aad' or 'aadd' in ask:
                        speak('Tell me what you have to do')
                        query = takeCommand().lower()
                        print(query)
                        task.append(query)
                    if 'reset' in ask:
                        speak('Congrats its all reset')
                        task.clear()
                    if 'no' in ask:
                        speak('No problem')
            else:
                for i in task:
                    speak(task[i])
    ###Program to open Camera
    elif 'open' and 'camera' in query:
        speak("Here's your camera.")
        subprocess.run('start microsoft.windows.camera:', shell=True)
    ### Program to open chrome
    elif 'open' and 'chrome' in query:
        speak("Here's your chrome")
        subprocess.run('start chrome', shell=True)
    ###Program to open calculator
    elif 'open' and 'calculator' in query:
        subprocess.run('C:\\Windows\\System32\\calc.exe', shell=True)
    ###Program to play some random music or play a user defined song
    elif 'play' and 'music' in query:
        speak("Which Song ?")
        music = takeCommand().lower()

        song_dir = 'F:\\Gaane (2019)'
        songs = os.listdir(song_dir)
        flag = 0
        print(music)

        if 'surprise me' in music:
            song_num = random.randint(1, len(songs) - 1)
            os.startfile(
                os.path.join(song_dir, songs[song_num])
            )
        else:
            for i in range(len(songs)):
                lst = (str(songs[i])).lower()
                if music in lst:
                    speak("Playing ")
                    speak(music)
                    flag = 1
                    os.startfile(
                        os.path.join(song_dir, songs[i])
                    )
                if (flag == 0):
                    speak("Sorry you don't have that song.")
    ###Current time program
    elif 'time' and 'now' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Its {str_time}")
    ###This program tells the covid stats when invoked
    elif 'covid' and 'stats' in query:
        speak('which country sir?')
        country = takeCommand().lower()
        covid = Covid()
        India_cases = covid.get_status_by_country_name(country)
        speak(India_cases)
        speak("Stay safe wear mask.")
     ###This program opens the source code of itself
    elif 'open your code' in query:
        speak('Admin system command line.')
        sys_cmd = takeCommand().lower()
        if sys_cmd == 'release recollection':
            os.startfile("C:\\Users\\Ryouzaaki\\PycharmProjects\\Cymon\\main.py")
            speak("Here's the system code.")
        else:
            speak("Sorry, wrong system command.")
###More Features will be added soon###
