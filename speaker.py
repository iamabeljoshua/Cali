# A python program that converts text to speech using tts
from ibm_watson import TextToSpeechV1

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import random

import os

import pyttsx3 


class TTSSpeaker(object):

    voice = "online"  # set to online to use ibm tts

    def __init__(self):

        #initialize offline tts
        self.pyttsxengine = pyttsx3.init()

        self.authenticator = IAMAuthenticator('1-D9_Ydjmq8Hg72JkLFBZTNWtC9i6X6NEb6LffHi2LBH')
        self.text_to_speech = TextToSpeechV1(
            authenticator=self.authenticator
        )

        self.text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/1915a1e6-e3b2-43a7-a600-91c6810567ac')

    def speak(self, input_texts):

        print(input_texts)

        if(TTSSpeaker.voice == "offline"):

            self.pyttsxengine.say(input_texts)
            self.pyttsxengine.runAndWait()

        else:

            filename = "ibmvoice.mp3"

            with open(filename, 'wb') as audio_file:
                audio_file.write(self.text_to_speech.synthesize(
                        input_texts,
                        voice='en-US_AllisonV3Voice',
                        accept='audio/mp3'
                    ).get_result().content)

            
            os.system("mpg321 "+ filename)
        