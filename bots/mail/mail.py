from ..bot import *
import pyautogui as mouse
from pykeyboard import PyKeyboard
import time


class MailBot(Bot):
    def __init__(self):
        self.app_name = "Mail.app"
        self.command = ""

    def work(self):
        # Open New Mail Application instance
        subprocess.call("open /Applications/" + self.app_name, shell=True)

        # Listen for Command
        while 1:
            self.command = listen().lower()
            if "finish" in self.command or "close" in self.command:
                speak("Closing Mail. See you again")
                break

            if "new" in self.command:
                send_new_email()
            elif "reply" in self.command:
                reply_email()
            else:
                speak("I don't know what you want? Can you speak again?")


def send_new_email():
    keyboard = PyKeyboard()
    # A New Mail pop up
    keyboard.press_keys(["Command", "N"])
    time.sleep(2)

    # The Destination Email
    mouse.typewrite("clearlove.96@gmail.com")
    time.sleep(2)

    # CC anyone
    mouse.press("tab")
    time.sleep(2)

    mouse.press("tab")
    time.sleep(1)

    # Subject of the Email
    mouse.typewrite("A Test Mail")
    time.sleep(2)

    mouse.press("tab")
    time.sleep(1)

    # Email Content
    mouse.typewrite("Some Content to send?")
    time.sleep(2)

    # Send Email
    keyboard.press_keys(["Command", "Shift", "D"])


def reply_email():
    keyboard = PyKeyboard()
    # Assume Email-to-Reply is chosen?
    # The Process of Finding The Email User want to reply will need some AI touching

    keyboard.press_keys(["Command", "R"])
    time.sleep(2)

    # The Content of Reply Email
    mouse.typewrite("Reply Content")
    time.sleep(2)

    # Send Email
    keyboard.press_keys(["Command", "Shift", "D"])
