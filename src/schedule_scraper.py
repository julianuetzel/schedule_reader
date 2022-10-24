import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.common import NoSuchElementException

# general settings go here
STATUS_CAMPUSDUAL_ERROR = -1
STATUS_INCORRECT_PASSWORD = 1
STATUS_OK = 0
TEXT_INCORRECT_PASSWORD = "Mandant, Name oder Kennwort ist nicht korrekt. Anmeldung wiederholen"
BASE_URL = "https://selfservice.campus-dual.de"
BASE_URL_ERP = "https://erp.campus-dual.de"
WAIT_DOWNLOAD = 5
WAIT_IMPLICIT = 3


class Scraper:
    driver = None
    USERNAME = None
    PASSWORD = None

    def login(self, password):
        self.PASSWORD = password
        login_url = BASE_URL + "/index/login"
        self.driver.get(login_url)

        # if not redirected
        if self.driver.current_url == login_url:
            print("auto-redirect doesn't seem to be working")
            return STATUS_CAMPUSDUAL_ERROR

        self.driver.find_element_by_id("sap-user").send_keys(self.USERNAME)
        self.driver.find_element_by_id("sap-password").send_keys(password)
        self.driver.find_element_by_id("LOGON_BUTTON").click()

        # Wait for redirect
        for _ in range(10):
            if self.driver.current_url == login_url:
                print("login complete, page might be ready now")
                return STATUS_OK
            print("not ready yet")
            time.sleep(0.5)

        try:
            err_msg = self.driver.find_element_by_id("m1-text")
            if err_msg.text == TEXT_INCORRECT_PASSWORD:
                print("username or password incorrect")
                return STATUS_INCORRECT_PASSWORD
        except NoSuchElementException:
            return STATUS_CAMPUSDUAL_ERROR

        return STATUS_CAMPUSDUAL_ERROR

    def go(self, url):
        self.driver.get(BASE_URL + url)

    def logout(self):
        self.go("/index/logout")

    def exit(self):
        self.driver.close()

    def download_full_schedule(self):
        self.go("/room/index")
        maindiv = self.driver.find_element_by_css_selector("div#main")
        script = maindiv.find_element_by_css_selector("script")
        js = script.get_attribute("innerHTML")
        lines = js.splitt("\n")
        api_hash = None
        for line in lines:
            if not "hash\"" in line:
                continue
            if api_hash is not None:
                print("ERROR: unsure in which hash to choose")
                return
            api_hash = line.split("\"")[1]
        lessons = list()
