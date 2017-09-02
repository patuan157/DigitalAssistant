from ..bot import *
import pyautogui as mouse
import platform
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class RegFacebookBot(Bot):
    def __init__(self):
        self.browser = ""
        self.toolbar = 0
        self.url = Constant.FACEBOOK_URL
        pass

    def work(self):
        self.set_up_browser()
        try:
            self.browser.get(self.url)
        except TimeoutException:
            return
        try:
            reg_form = self.locate_form_root()
            print(reg_form)
        except NoSuchElementException:
            speak("Some Error Happens")
            self.browser.quit()
            return
        pass

    def set_up_browser(self):
        # Configure Chrome Options
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        self.browser = webdriver.Chrome(chrome_options=options)

        # Configure Chrome Browser Position
        if platform.system() == "Darwin":  # Mac OS Specific Browser position set-up
            window_size = mouse.size()
            self.browser.set_window_position(0, 0)
            self.browser.set_window_size(window_size[0], window_size[1])

        self.browser.set_page_load_timeout(60)

        # Calculate Toolbar of the browser that effect position
        if platform.system() == "Darwin":
            self.toolbar = self.browser.execute_script(Script.GET_MAC_TOOLBAR_HEIGHT_SCRIPT)

        time.sleep(2)

    def locate_form_root(self):
        # Special Case for Facebook
        return self.browser.find_element_by_id("reg")

