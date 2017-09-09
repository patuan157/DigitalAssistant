from ..bot import *
import pyautogui as mouse
import time
from pykeyboard import PyKeyboard


class TelegramBot(Bot):
    def __init__(self):
        self.app_name = "Telegram"
        self.command = ""

    def work(self):
        # Open New WhatsApp Instance instance
        subprocess.call("open /Applications/" + self.app_name + ".app", shell=True)
        time.sleep(5)           # Ensure the App open and load fully

        # Listen for Command
        speak("What would you like to do")
        while 1:
            # Ask for command. Will close if no input (twice)
            self.command = listen_for_input_with_timeout().lower()

            if self.command == "timeout" or self.command == "noise":
                speak("I do not receive any command. Are you there?")
                command = listen_for_input_with_timeout().lower()
                if command == "timeout" or command == "noise":
                    speak("You might be busy. I will close Telegram for now")
                    self.close()
                    return 0                    # Return status : 0 - No input lead to Closing App

            if "no" in self.command or "nothing" in self.command or \
                    "finish" in self.command or "close" in self.command:         # Closing Application
                speak("Closing Telegram as you wish")
                self.close()
                return 1

            if "send" in self.command and "message" in self.command:        # Command : "Send Message"
                # Send New Message to Someone
                send_new_message()
                speak("Any other command?")
            elif "check" in self.command and "message" in self.command:     # Command : "Check Message"
                # Collect Chat Log
                check_message()
                speak("Any other command?")
            else:
                speak("Unable to hear you clearly.  Could you speak again?")
            time.sleep(0.5)

    def close(self):
        subprocess.call("osascript -e 'quit app \"" + self.app_name + "\"'", shell=True)


def send_new_message():
    # Search That User
    keyboard = PyKeyboard()

    speak("Send to who?")
    user = listen_for_input_without_timeout()
    # user = "Ng Wee Keong"

    keyboard.press_keys(["Command", "K"])
    time.sleep(1)

    mouse.typewrite(user)
    mouse.press("enter")
    time.sleep(2)

    # Insert the Message to Send
    speak("Speak your text please")
    message = listen_for_input_without_timeout()
    # message = "This Message to test if the Bot work correctly"
    mouse.typewrite(message)
    time.sleep(2)

    # Send Message
    mouse.press("enter")


def check_message():
    # Search That User
    keyboard = PyKeyboard()

    speak("To whom will I check?")
    user = listen_for_input_without_timeout()
    # user = "Ng Wee Keong"

    keyboard.press_keys(["Command", "K"])
    time.sleep(1)

    mouse.typewrite(user)
    time.sleep(1)
    mouse.press("enter")
    time.sleep(2)

    # Confirm Go Into Chat Log
    speak("Here is " + user + " messages")


