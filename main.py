# Main Calistol proram file: connects other components together.
import speech_recognition as sr

from speaker import * 

from timeservice import * 

from weather import *

from util import * 

import re

import json


#the following functions uses regex to match recognized text to validate actions to take.



def is_twitter_profile_action(recognized_text):

    #demonstrates how to use regex for pattern matching and extraction.

    pattern = "open up (\S+) on twitter"

    matches = re.findall(pattern, recognized_text, re.IGNORECASE)

    return len(matches) > 0


def is_youtube_search_action(recognized_text):

    text = recognized_text.lower() #convert everything to lower case

    return "search for" in text and "on youtube" in text


def extract_youtube_search_term(recognized_text):

    text = recognized_text.lower()

    text = text.replace("search for","")

    text = text.replace("on youtube","")

    return text.strip() #remove any leading or trailing whitespace
    

def get_twitter_profile(recognized_text):
    pattern = "open up (\S+) on twitter"

    matches = re.findall(pattern, recognized_text, re.IGNORECASE)

    return matches[0]


def is_weather_search_action(recognized_text):
    
    text = recognized_text.lower() #convert everything to lower case

    return "what is the weather in" in text


def extract_city_name_for_weather_action(recognized_text):

    text = recognized_text.lower()

    return text.replace("what is the weather in","").strip()



def main():

    tts_speaker = TTSSpeaker()

    recognizer = sr.Recognizer()


    while True:

        with sr.Microphone() as source:
            print("Say something!")
            audio = recognizer.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
            audio = recognizer.listen(source)                   # now when we listen, the energy threshold is already set to a good value, and we can reliably catch speech right away

        # Speech recognition using Google Speech Recognition
        
        try:
            # To use your API Key use: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`

            recognized_text  = recognizer.recognize_google(audio)

            print("You said: " + recognized_text)

            #Here we will use simple if statements to map the captured text to appropriate actions.

            if "local time" in recognized_text:
                tts_speaker.speak(TimeService().get_local_time())

            #should open a twitter profile?, sentence to match: open up iamabeljoshua on twitter. 
            if is_twitter_profile_action(recognized_text):

                open_page("https://twitter.com/" + get_twitter_profile(recognized_text))
                
            #should open a youtube search page?, sentence to match: search for {searchterm} on youtube
            if is_youtube_search_action(recognized_text):

                open_page("https://www.youtube.com/results?search_query=" + extract_youtube_search_term(recognized_text))

            #should fetch weather data for a particular city?
            if is_weather_search_action(recognized_text):

                tts_speaker.speak(WeatherService().get_weather_data(extract_city_name_for_weather_action(recognized_text)))
                
            else:
                tts_speaker.speak("I am sorry. I didn't get that!. There is no procedure available to handle your request")

        except sr.UnknownValueError:
            tts_speaker.speak("I am sorry. I didn't get that!")
            print("Google Speech Recognition could not understand audio")
            
        except sr.RequestError as e:
            tts_speaker.speak("I am sorry. I didn't get that!")
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":

    main() 