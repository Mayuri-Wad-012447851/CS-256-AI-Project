from bs4 import BeautifulSoup as Soup
from Job import *
import urllib
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

class HandshakeScraper(object):

    jobsFetched = []

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def start(self):
        url = "https://sjsu.okta.com/login/login.htm?fromURI=%2Fapp%2Fsanjosestateuniversity_sjsuhandshake_1%2Fexk5536is1LPSizqM0x7%2Fsso%2Fsaml%3FSAMLRequest%3DnZNdT8IwFIbv%252FRVL72EdwoSGLcERIwkqgemFN6brztx0a2dPp%252FjvLZ8hgWDCZb%252Fe97zPOR0ir8qajRqTyzl8NYDGWValRLY%252BCEijJVMcC2SSV4DMCLYYPUxZp01ZrZVRQpXEmYwDkmZ%252B4me8m6Y97iXUS%252FrdpJfc%252BFmSDuCGChj0wff6HcGJ8wIaCyUDYmXsa8QGJhINl8ZuUc9v0V6rQ%252BMOZXTArukrcWZbr9tCpoV8P19YsrmE7D6OZ63Z0yImzggRtLGmkZLYVKAXoL8LAc%252FzaUByY2pkrsvruv2hCplzmWLOP6EtVOWuULyJzTMSDldLtq5ZH7A6XxHfuZPwH6966B4YhFfDTYcereRkPFNlIX4v6dCd0hW3dC2IslQ%252FkQZuICBGN6tI7rHJ3nk7FpCuh8TSM7C8aEgiVdVcF7jqOyy5MDuWh8JRaVHNIbuE7JbcKbl9xJNpbFb3%252BCOEfw%253D%253D"

        driver = webdriver.Chrome('./chromedriver_win32/chromedriver')

        driver.get(url)

        self.handshake_login(driver)
        self.navigate_to_jobs(driver)
        self.enter_keyword_and_location(driver)
        self.fetch_jobs(driver)

    def fetch_jobs(self, driver):
        current_url = driver.page_source
        driver.get(current_url)
        html = driver.page_source
        target = Soup(html,"html.parser")
        print str(target)

    def enter_keyword_and_location(self,driver):
        elem = driver.find_element(By.CLASS_NAME, "clear")
        elem.click()

        elem = driver.find_element(By.ID,"query")
        elem.send_keys("Computer Science")
        elem.send_keys(Keys.ENTER)
        elem.send_keys(Keys.TAB)
        elem.send_keys(Keys.TAB)
        time.sleep(5)

    def navigate_to_jobs(self, driver):
        driver.get("https://sjsu.joinhandshake.com/postings")
        time.sleep(3)

    def handshake_login(self, driver):
        time.sleep(3)

        elem = driver.find_element(By.ID, "okta-signin-username")
        elem.send_keys(self.username)
        elem = driver.find_element(By.ID, "okta-signin-password")
        elem.send_keys(self.password)
        # Enter credentials with Keys.RETURN
        elem.send_keys(Keys.ENTER)
        # Wait a few seconds for the page to load
        time.sleep(8)