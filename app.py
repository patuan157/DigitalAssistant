import time
import sys

from bots.autoreg.reg_facebook import RegFacebookBot
from bots.autoreg.reg_google import RegGoogleBot
from bots.mail.mail import MailBot
from bots.message.telegram import TelegramBot
from bots.message.whatsapp import WhatsAppBot
from bots.netsurf.surf_cnn import SurfCnnBot
from bots.bot import *


def main():
    time.sleep(1)
    speak("Hello. Welcome to Johnson, your Digital Assistant")
    time.sleep(1)
    speak("What can I help you?")
    status = 1                              # 1 : With Timeout and 0 : Without Timeout

    while 1:
        if status == 0:
            command = listen_for_input_without_timeout().lower()            # Listen until have input
        else:
            command = listen_for_input_with_timeout().lower()               # Listen for input until timeout
            # Handle Un-response case
            # Will repeat to ask 1 time and chill after that
            if command == "timeout" or command == "noise":
                speak("I did not hear you. Are you there?")
                command = listen_for_input_with_timeout().lower()
                if command == "timeout" or command == "noise":
                    speak("Looks like you are busy now. I will wait until you speak")
                    command = listen_for_input_without_timeout().lower()

        # To a certain point, you will receive a command input
        bot = decode_command(command)
        if bot == "Close Application":
            time.sleep(1)
            speak("Good bye")
            break
        elif bot == "Unknown Command":
            time.sleep(1)
            speak("Sorry, can you repeat?")
        else:
            status = bot.work()
            time.sleep(1)
            if status == 0:
                speak("Looks like you are busy now. I will wait until you speak")
            elif status == 1:
                speak("What else can I help you?")


def speak_practice():
    speak("up")
    while 1:
        inp = (listen_for_input_without_timeout())
        print(inp)
        speak(inp)


def decode_command(command):
    if "mail" in command:
        bot = MailBot()
        return bot
    elif "telegram" in command:
        bot = TelegramBot()
        return bot
    elif "whatsapp" in command:
        bot = WhatsAppBot()
        return bot
    elif "google" in command:
        bot = RegGoogleBot()
        return bot
    elif "facebook" in command:
        bot = RegFacebookBot()
        return bot
    elif "cnn" in command:
        bot = SurfCnnBot()
        return bot
    elif "close" in command:
        return "Close Application"
    else:
        return "Unknown Command"


if __name__ == "__main__":
    if sys.argv[1] == "Practice":
        speak_practice()
    else:
        main()

