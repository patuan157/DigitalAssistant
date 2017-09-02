import pyautogui as mouse
import time
import subprocess
from pykeyboard import PyKeyboard

subprocess.call("open /Applications/" + "Telegram.app", shell=True)
time.sleep(3)

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
# mouse.press("enter")
