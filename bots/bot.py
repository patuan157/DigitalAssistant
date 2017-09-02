import speech_recognition as sr
import subprocess
from abc import ABCMeta


class Bot:
    __metaclass__ = ABCMeta

    def work(self):
        pass


class Script(object):
    # MAC Toolbar Height Chrome
    GET_MAC_TOOLBAR_HEIGHT_SCRIPT = "return window.outerHeight - window.innerHeight + window.screenTop"


class Constant(object):
    # Specific Registration URL (Social Media)
    GOOGLE_URL = "https://accounts.google.com/SignUp?hl=en-GB"
    FACEBOOK_URL = "http://facebook.com"
    TWITTER_URL = "https://twitter.com/signup"
    INSTAGRAM_URL = "https://www.instagram.com/accounts/emailsignup/?signupFirst=true"


def speak(text):
    subprocess.call("say " + text, shell=True)


def listen():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            audio = r.listen(source)
        audio_text = r.recognize_google(audio_data=audio)
        return audio_text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
