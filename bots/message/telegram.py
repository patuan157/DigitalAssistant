from ..bot import *
import pyautogui as mouse
import time
from pykeyboard import PyKeyboard


class TelegramBot(Bot):
    def __init__(self):
        self.app_name = "Telegram.app"
        self.command = ""

    def work(self):
        # Open New WhatsApp Instance instance
        subprocess.call("open /Applications/" + self.app_name, shell=True)
        time.sleep(10)           # Ensure the App open and load fully

        # Listen for Command
        while 1:
            self.command = listen().lower()
            if "finish" in self.command or "close" in self.command:
                speak("Closing WhatsApp. See you again")
                break

            if "send" in self.command and "message" in self.command:
                # Send New Message to Someone
                send_new_message()
            elif "chat log" in self.command:
                # Collect Chat Log
                collect_chat_log()
            else:
                speak("I don't know what you want? Can you speak again?")


def send_new_message():
    # To Whom which I will send?
    # user = listen()

    # Search That User
    keyboard = PyKeyboard()
    keyboard.press_keys(["Command", "K"])
    time.sleep(1)

    mouse.typewrite("Ng Wee Keong")
    mouse.press("enter")
    time.sleep(2)

    # Insert the Message to Send
    message = "This Message to test if the Bot work correctly"
    mouse.typewrite(message)

    # Send Message
    mouse.press("enter")


def collect_chat_log():
    pass

