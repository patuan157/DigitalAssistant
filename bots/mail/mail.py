from ..bot import *
import pyautogui as mouse
from pykeyboard import PyKeyboard
import time


class MailBot(Bot):
    def __init__(self):
        self.app_name = "Mail"
        self.command = ""

    def work(self):
        # Open New Mail Application instance
        subprocess.call("open /Applications/" + self.app_name + ".app", shell=True)
        time.sleep(5)

        # Listen for Command
        speak("What would you like to do")
        while 1:
            # Ask for command. Will close if no input (twice)
            self.command = listen_for_input_with_timeout().lower()

            if self.command == "timeout" or self.command == "noise":
                speak("I do not receive any command. Are you there?")
                command = listen_for_input_with_timeout().lower()
                if command == "timeout" or command == "noise":
                    speak("You might be busy. I will close Mail for now")
                    self.close()
                    return 0                    # Return status : 0 - No input lead to Closing App

            if "no" in self.command or "nothing" in self.command or \
                    "finish" in self.command or "close" in self.command:         # Closing Application
                speak("Closing Mail as you wish")
                self.close()
                return 1

            if "new" in self.command:                   # Command : Send new email
                send_new_email()
                speak("Any other action?")
            elif "check" in self.command:               # Command : Check Email (+ Reply command inside)
                check_email()
                speak("Any other action")
            else:
                speak("Unable to hear you clearly.  Could you speak again?")
            time.sleep(0.5)

    def close(self):
        subprocess.call("osascript -e 'quit app \"" + self.app_name + "\"'", shell=True)


def send_new_email():
    keyboard = PyKeyboard()
    # A New Mail pop up
    keyboard.press_keys(["Command", "N"])
    time.sleep(2)

    # The Destination Email
    speak("To whom will I send?")
    receiver = listen_for_input_without_timeout()
    # receiver = "Phan Anh Tuan"

    if "wee keong" in receiver.lower():
        mouse.typewrite("wkn@gmail.com")
    elif "tuan" in receiver.lower():
        mouse.typewrite("clearlove.96@gmail.com")
    # mouse.typewrite("clearlove.96@gmail.com")
    time.sleep(2)

    # CC anyone
    mouse.press("tab")
    time.sleep(2)

    mouse.press("tab")
    time.sleep(1)

    # Subject of the Email
    speak("Which is the subject of the mail?")
    subject = listen_for_input_without_timeout()
    mouse.typewrite(subject)
    time.sleep(2)

    mouse.press("tab")
    time.sleep(1)

    # Email Content
    speak("Which is the content of the mail")
    content = listen_for_input_without_timeout()
    mouse.typewrite(content)
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
    speak("What will I reply")
    content = listen_for_input_without_timeout()
    mouse.typewrite(content)
    time.sleep(2)

    # Send Email
    keyboard.press_keys(["Command", "Shift", "D"])


def check_email():
    # Confirm Navigate down the mail
    speak("I am inside your list of email right now")
    # Move mouse to center of screen
    screen = mouse.size()
    mouse.moveTo(screen[0]//2, screen[1]//2, duration=0.5)
    while 1:
        action = listen_for_input_without_timeout().lower()
        if "down" in action or "one" in action or "a" in action:
            mouse.press("down")
        elif "up" in action or "two" in action or "b" in action:
            mouse.press("up")
        elif "scroll" in action or "three" in action or "c" in action:
            scroll("Down")
        elif "one" in action:
            scroll("Up")
        elif "reply" in action:
            # Reply current email
            reply_email()
        elif "new email" in action:
            # Send new email
            send_new_email()
        elif "finish" in action:
            speak("Finish checking your mail")
            break
        else:
            speak("Can you speak again?")
