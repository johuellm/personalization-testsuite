from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import os
import time


class Scraper:
    """
    Creates a Selenium Webbrowser instance and retrives Data from websites
    """

    def __init__(self, path, headless=False, proxy=None, geckopath="geckodriver.exe"):
        """
        Init of the Scraper

        :param path: a Profile Path of a Firefox Profile
        :param headless: Argument determining the headless execution, default = False
        :param proxy: A String for a Proxy of format "IP:Port", default = None

        1.)Setting Attributes for the Selenium driver
        -profilepath: Path to a profile that shall be used by the driver
        -headless: boolen that determines whether execution in the Browser will be shown. default = false
        -proxy: gives option to select a Proxy; default = none

        2.) Result Attributes (scraped information)
        -source: sourcecode of the scraped webpage
        -imagepath: path to a made screenshot
        -treuurl: retrieved url (may have changed after calling the website)
        -cookies: retrieved cookies
        """

        self.profilepath = path
        self.headless = headless
        self.proxy = proxy
        self.geckopath = geckopath

        self.source = ""
        self.imagepath = ""
        self.trueurl = ""
        self.cookies = ""

    def headless(self, state):
        """changes headless attribute"""
        self.headless = state

    def proxy(self, proxy):
        """changes Proxy attribute"""
        self.proxy = proxy

    def get_source(self):
        """ get function for the Source"""
        return self.source

    def get_imagepath(self):
        """get function for the imagePath"""
        return self.imagepath

    def get_trueurl(self):
        """get function for the  trueurl"""
        return self.trueurl

    def get_cookies(self):
        """get function for self.cookies"""
        return self.cookies

    def execute(self, url):
        """
        Creates a selenium webbrowser-instance( with the profile and options set in the attributes)
        and retrieves Data from Website

        :param url: The Url ist the Target on which the included actions will be performed on
        The results will be stored in class attributes
        """

        """Creation of Webbrowser instance"""
        profile = FirefoxProfile(self.profilepath)
        profile.set_preference("network.cookie.cookieBehavior", 0)
        profile.update_preferences()
        options = Options()
        options.headless = self.headless
        browser = webdriver.Firefox(firefox_profile=profile, options=options, executable_path=self.geckopath)
        browser.get(url)

        """Retrieval of Data"""

        """Get Sourcecode"""
        self.source = browser.page_source
        """Get the currently used URL"""
        self.trueurl = browser.current_url
        """Get Cookies from the opened website"""
        self.cookies = browser.get_cookies()

        """make screenshots of the page"""
        time.sleep(3)
        self.imagepath = str(os.path.abspath(os.getcwd())) + '\screenshot' + str(self)[-19:-1] + '.png'
        browser.save_screenshot(self.imagepath)
        """quit Browser to clear temporary storage"""
        browser.quit()
