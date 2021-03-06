from ..bot import *
import pyautogui as mouse
import platform
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains


class RegFacebookBot(Bot):
    def __init__(self):
        self.browser = None
        self.toolbar = 0
        self.url = Constant.FACEBOOK_URL

    def work(self):
        self.set_up_browser()
        try:
            self.browser.get(self.url)
        except TimeoutException:
            return
        try:
            reg_form = self.locate_form_root()
            self.handle_text_input(reg_form)
            self.choose_birth_day(reg_form)
            self.choose_gender(reg_form)
            self.submit_form(reg_form)
            time.sleep(5)
            speak("Complete the Registration on Facebook")
            self.browser.quit()
        except NoSuchElementException:
            speak("Some Error Happens")
            self.browser.quit()
            return

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

    def handle_text_input(self, form):
        """
        Collect all the Text Input Field to evaluate their context and fill them
        """
        text_inputs = form.find_elements_by_tag_name("input")
        # ["text", "password", "tel", "email"] is type for text input
        for text_field in text_inputs:
            if text_field.get_attribute("type") in ["text", "password", "tel", "email"]:
                try:
                    self.fill_text_input(text_field)
                except WebDriverException:
                    pass

    @staticmethod
    def fill_text_input(text_field):
        """
        Fill The Text Field depends on the context of that input
        """
        input_name = text_field.get_attribute("name").lower()

        if "name" in input_name:
            if "first" in input_name:                               # First Name Field
                result = Profile.FIRST_NAME
            elif "last" in input_name or "sur" in input_name:       # Last Name or Sur Name Field
                result = Profile.LAST_NAME
            elif "user" in input_name or "account" in input_name:   # User Name or Account Name Field
                result = Profile.USERNAME
            elif "full" in input_name:                              # Full Name Field
                result = Profile.FULL_NAME
            else:                                                   # Only Name required
                result = Profile.FULL_NAME

        elif "mail" in input_name:
            result = Profile.EMAIL                                  # Email Field

        elif "passwd" in input_name or "password" in input_name:
            result = Profile.PASSWORD                               # Password and Re-enter Password Field

        elif "birth" in input_name:                                 # Birthday Input as Text Field
            if "month" in input_name:
                speak("What is your birth month?")
                # result = Profile.BIRTH_MONTH_S
                result = listen_for_input()
            elif "year" in input_name:
                speak("What is your birth year?")
                # result = Profile.BIRTH_YEAR
                result = listen_for_input()
            else:
                speak("What is your birth day")
                # result = Profile.BIRTHDAY
                result = listen_for_input()

        elif "sex" in input_name or "gender" in input_name:
            speak("What is your gender")
            # result = Profile.GENDER                                 # Gender Input as Text Field
            result = listen_for_input()

        elif "phone" in input_name:                                 # Phone Number Field
            speak("What is your phone number")
            result = Profile.PHONE

        elif "captcha" in input_name:                               # Captcha, which can't be handle
            return
        else:
            return

        text_field.clear()
        text_field.send_keys(result)

    @staticmethod
    def choose_birth_day(form):
        birth_day = form.find_element_by_id("day")
        speak("What is your birthday")
        day = listen_for_input()
        # Select(birth_day).select_by_value(Profile.BIRTHDAY)
        Select(birth_day).select_by_value(day)

        birth_month = form.find_element_by_id("month")
        speak("What is your birth month")
        month = listen_for_input()          # Input as number
        # Select(birth_month).select_by_value(Profile.BIRTH_MONTH_N)
        Select(birth_month).select_by_value(month)

        birth_year = form.find_element_by_id("year")
        speak("What is your birth year")
        year = listen_for_input()
        # Select(birth_year).select_by_value(Profile.BIRTH_YEAR)
        Select(birth_year).select_by_value(year)

    def choose_gender(self, form):
        # Radio Buttons to choose Gender
        radio_buttons = form.find_elements_by_xpath("//input[@type='radio']")
        # The Context That Group Radio Button focus
        radio_buttons_name = []

        for button in radio_buttons:
            button_name = button.get_attribute("name").lower()
            if button_name != "" and button_name not in radio_buttons_name:
                radio_buttons_name.append(button_name)

        for name in radio_buttons_name:
            if "sex" in name or "gender" in name:
                speak("What is your gender")
                gender = listen_for_input()
                # sex = form.find_element_by_xpath("//*[text()='" + Profile.GENDER + "']")
                sex = form.find_element_by_xpath("//*[text()='" + gender + "']")
                ActionChains(self.browser).move_to_element(sex).click().perform()

    def submit_form(self, form):
        pass

