from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, \
    StaleElementReferenceException, NoSuchElementException

import pyautogui as mouse
import time
import random
import platform

from ..bot import *


class SurfCnnBot(Bot):
    def __init__(self, category=None, keyword=None):
        self.browser = None
        self.url = Constant.CNN_URL
        self.category = category if category is not None else None
        self.keyword = keyword if keyword is not None else None

        self.domain = "cnn.com"
        self.toolbar = 0

    def work(self):
        self.set_up_browser()
        self.choose_category()
        self.choose_keyword()
        self.visit_page()
        while 1:
            speak("What will we do next?")
            next_action = listen_for_input().lower()
            if "next page" in next_action:
                self.choose_next_link()
                self.visit_page()
            elif "go back" in next_action:
                try:
                    self.browser.back()
                except WebDriverException:
                    pass
                time.sleep(1)
                self.url = self.browser.current_url
            elif "finish" in next_action or "close":
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

    def choose_category(self):
        speak("Which category do you want")
        self.category = listen_for_input().lower()
        if "opinion" in self.category:
            self.url = Constant.CNN_OPINION_URL
        elif "sport" in self.category:
            self.url = Constant.CNN_SPORT_URL
        elif "travel" in self.category:
            self.url = Constant.CNN_TRAVEL_URL
        elif "style" in self.category:
            self.url = Constant.CNN_STYLE_URL
        elif "money" in self.category:
            self.url = Constant.CNN_MONEY_URL
        elif "health" in self.category:
            self.url = Constant.CNN_HEALTH_URL
        elif "entertainment" in self.category:
            self.url = Constant.CNN_ENTERTAINMENT_URL
        elif "technology" in self.category:
            self.url = Constant.CNN_TECHNOLOGY_URL
        else:
            speak("No category specified.")

    def choose_keyword(self):
        speak("What keyword for this session?")
        self.keyword = listen_for_input().lower()

    def visit_page(self):
        try:
            self.browser.get(self.url)
        except TimeoutException:
            pass

        time.sleep(1)
        scroll_sequence = random.choice(Constant.PAGE_SCROLL_SEQUENCE)
        for action in scroll_sequence:
            if action == "D":
                time.sleep(2)
                ActionChains(self.browser).send_keys(Keys.PAGE_DOWN).perform()
            elif action == "U":
                time.sleep(2)
                ActionChains(self.browser).send_keys(Keys.PAGE_UP).perform()

    def choose_next_link(self):
        """
        Manage to choose next Page to navigate in the session
        Make Random decision for any url in current page
        """
        list_urls = self.get_list_link()

        # While loop to choose link in same domain
        while 1:
            # System Secure Random Method
            secure_random = random.SystemRandom()
            # Random a links and update instance's url
            url_element = secure_random.choice(list_urls)
            self.url = url_element.get_attribute("href")

            if self.is_link_in_same_domain():
                break

    def get_list_link(self):
        # List Visible URL on current Page
        list_links = self.browser.find_elements_by_tag_name("a")
        # Remove duplicates URL and choose visible link
        list_urls = []

        if self.keyword is not None:              # Consider Topic when return list link
            for link in list_links:
                try:
                    href_attribute = link.get_attribute("href")
                    text_content = link.text
                    if href_attribute is not None:
                        if link not in list_urls and link.is_displayed() \
                                and self.is_keyword_appear(href_attribute, text_content):
                            list_urls.append(link)
                except StaleElementReferenceException:
                    continue

        if len(list_urls) > 0:                  # While more than 1 link relate to topic, return it
            return list_urls

        for link in list_links:                 # Or we will return a general list link anyway
            if link not in list_urls and link.is_displayed():
                list_urls.append(link)

        return list_urls

    def is_keyword_appear(self, url, text_content):
        # length_keyword = len(self.keyword)
        # keyword_str = self.keyword[1:length_keyword-1]
        # list_keyword = keyword_str.split(",")
        # for keyword in list_keyword:
        #     if keyword.lower() in url:
        #         return True

        # for keyword in list_keyword:
        #     keyword = keyword.replace("-", " ")
        #     if keyword.lower() in text_content:
        #         return True

        if self.keyword.lower() in text_content:
            return True
        elif self.keyword.lower() in url:
            return True
        return False

    def is_link_in_same_domain(self):
        if self.category == "Opinion":
            return self.domain in self.url and "opinion" in self.url
        elif self.category == "Sport":
            return self.domain in self.url and "sport" in self.url
        elif self.category == "Travel":
            return self.domain in self.url and "travel" in self.url
        elif self.category == "Style":
            return self.domain in self.url and "style" in self.url
        elif self.category == "Money":
            return self.domain in self.url and "money" in self.url
        elif self.category == "Health":
            return self.domain in self.url and "health" in self.url
        elif self.category == "Entertainment":
            return self.domain in self.url and "entertainment" in self.url
        elif self.category == "Technology":
            return self.domain in self.url and "technology" in self.url
        else:
            return self.domain in self.url

    def share_article(self):
        if "money.cnn.com" in self.url:  # Specific Share Button for CNN Money
            facebook_share = self.browser.execute_script(Script.GET_CNN_MONEY_FACEBOOK_SHARE_BUTTON_SCRIPT)
        else:  # Other Page has same button?
            facebook_share = self.browser.execute_script(Script.GET_CNN_FACEBOOK_SHARE_BUTTON_SCRIPT)

        if len(facebook_share) != 0:
            speak("This page can be share in Facebook?. Do you want to share it?")
            answer = listen_for_input()
            if "yes" in answer:
                self.browser.execute_script("document.body.scrollTop = 0")  # Scroll Back to Top for visible share
                time.sleep(1)
                for button in facebook_share:
                    if button.is_displayed():
                        button.click()
                        break
                # New Window will pop-up ask to share article to Facebook
                time.sleep(5)
                window_before = self.browser.window_handles[0]
                window_after = self.browser.window_handles[1]
                # Change to Pop-up window and Login Facebook
                self.browser.switch_to_window(window_after)
                try:
                    time.sleep(1)
                    self.browser.find_element_by_id("email").send_keys(Constant.FACEBOOK_LOGIN_EMAIL)
                    time.sleep(1)
                    self.browser.find_element_by_id("pass").send_keys(Constant.FACEBOOK_LOGIN_PASS)
                    time.sleep(1)
                    ActionChains(self.browser).send_keys(Keys.ENTER).perform()
                except NoSuchElementException:
                    # print("Already Login")
                    pass
                time.sleep(5)
                # Find Post Button and Post
                post_button = self.browser.find_element_by_xpath("//span[text()='Post to Facebook']")
                post_button.click()
                time.sleep(5)
                # Let the Post process and switch back to Main browser
                self.browser.switch_to_window(window_before)
                time.sleep(3)
            else:
                pass
