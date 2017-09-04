import time

from bots.autoreg.reg_facebook import RegFacebookBot
from bots.autoreg.reg_google import RegGoogleBot
from bots.mail.mail import MailBot
from bots.message.telegram import TelegramBot
from bots.message.whatsapp import WhatsAppBot
from bots.netsurf.surf_cnn import SurfCnnBot
from bots.bot import *


def main():
    time.sleep(1)
    speak("Hello. Welcome to Digital Assistant")
    time.sleep(3)
    speak("What can I help you?")

    while 1:
        command = listen_for_input().lower()
        bot = decode_command(command)
        if bot == "Close Application":
            speak("Good bye")
            break
        elif bot == "Unknown Command":
            speak("Can you repeat command ?")
        else:
            bot.work()
            speak("What else can I help you?")

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
    elif "close digital assistant":
        return "Close Application"
    else:
        return "Unknown Command"


if __name__ == "__main__":
    main()
