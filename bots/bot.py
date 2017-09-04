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

    # CNN Facebook Share Button
    GET_CNN_FACEBOOK_SHARE_BUTTON_SCRIPT = "return document.getElementsByClassName('gig-button-container-facebook');"

    # CNN Money site Facebook Share Button
    GET_CNN_MONEY_FACEBOOK_SHARE_BUTTON_SCRIPT = "return document.getElementsByClassName('js-share-fb')"


class Constant(object):
    # Specific Registration URL (Social Media)
    GOOGLE_URL = "https://accounts.google.com/SignUp?hl=en-GB"
    FACEBOOK_URL = "http://facebook.com"
    TWITTER_URL = "https://twitter.com/signup"
    INSTAGRAM_URL = "https://www.instagram.com/accounts/emailsignup/?signupFirst=true"

    # CNN Sub_Page url
    CNN_URL = "http://edition.cnn.com/"
    CNN_OPINION_URL = "http://edition.cnn.com/opinions"
    CNN_SPORT_URL = "http://edition.cnn.com/sport"
    CNN_TRAVEL_URL = "http://edition.cnn.com/travel"
    CNN_STYLE_URL = "http://edition.cnn.com/style"
    CNN_MONEY_URL = "http://money.cnn.com/"
    CNN_HEALTH_URL = "http://edition.cnn.com/health"
    CNN_ENTERTAINMENT_URL = "http://edition.cnn.com/entertainment"
    CNN_TECHNOLOGY_URL = "http://money.cnn.com/technology/"

    PAGE_SCROLL_SEQUENCE = [["D", "D", "U", "D", "D", "D", "U"], ["D", "D", "D", "U", "U", "D", "D", "U"],
                            ["D", "U", "D", "D", "U", "D", "D"], ["D", "U", "D", "D", "D", "U", "D", "U"],
                            ["D", "D", "U", "D", "U", "D", "D"], ["D", "D", "U", "D", "D", "D", "U", "D"]]

    # Information To Login Facebook
    FACEBOOK_LOGIN_EMAIL = "clearlove.157@gmail.com"
    FACEBOOK_LOGIN_PASS = "Patuan1996"


class Profile(object):
    """
    Set Constants Variables
    """
    FIRST_NAME = "Phan"
    LAST_NAME = "Anh Tuan"
    FULL_NAME = "Phan Anh Tuan"
    EMAIL = "clearlove.96@gmail.com"
    USERNAME = "pat_unique_1996"
    PASSWORD = "p@ssW0RD1996"
    BIRTHDAY = "15"
    BIRTH_MONTH_S = "July"
    BIRTH_MONTH_N = "7"
    BIRTH_YEAR = "1996"
    GENDER = "Male"
    PHONE = "+65 97742291"


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


def listen_for_input():
    inp = ""
    while inp == "":
        inp = listen()

    return inp
