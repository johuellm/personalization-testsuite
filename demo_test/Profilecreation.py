from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from random import randint
import time
import shutil
import os


class Profiles:
    """
    Class for the Creation of Firefoxprofiles
    """
      
    def __init__(self, geckopath='geckodriver.exe'):
        """
        :param geckopath: path where the firefox Geckodriver is stored
        -useragents: List of Useragent for the preferences
        -proxies: List of Proxies to be set in the preferences
        -numberofprofiles: Number of Profiles that shall be created
        -startpages: Startpages for seting related preferences
        -paths: List with the Paths of the created profiles
        """
        
        self.useragents = [
                            "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729) (Prevx 3.0.5)",
                            "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1) ",
                            "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
                            "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
                            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
                            "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536",
                            "Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36",
                            "Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36",
                            "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
                            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
                            "Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+"
                            ]
        self.proxies = []
        self.startpages = ["http://www.google.com", "https://www.ecosia.org", "https://www.bing.com", "https://www.duckduckgo.com"]
        self.paths = []
        self.geckopath = geckopath

    def get_paths(self):
        """return function for Paths"""
        return self.paths

    def create(self, nop=5):
        """
        Function for the Creation of Profiles
        :param nop: the number of Profiles that get created (default 5)
        !!!Due to the assignment of user agents nop s currently limeted to 12. For more you need
        to change the assignment in line 68!!!
        The Paths of the resulting Profiles are stored in the attribute self.paths

        The Try except clauses will always lead to the except clause as the filesystem returns an error,
        but why ever the filesystem still does the operations it says it can't.


        """
        numberofprofiles = nop
        for i in range(1, (numberofprofiles + 1)):
            print("Profile ", i, " wird erstellt")
            profile = FirefoxProfile()

            """User Agent Preferences"""
            profile.set_preference("general.useragent.override", self.useragents[i])
            print(f"Preference for {i} is {self.useragents[i]}")
            # self.useragents[randint(0, len(self.useragents)-1)])

            """set startpage which is opening when the Browser is started"""
            profile.set_preference("browser.startup.homepage", self.startpages[randint(0, len(self.startpages)-1)])

            """set Proxy Settings"""
            # profile.set_preference('network.proxy.type', 1)
            # profile.set_preference('network.proxy.socks', ip)
            # profile.set_preference('network.proxy.socks_port', int(port))

            """set signon settings. True, as we do not want to need to always sign on """
            # profile.set_preference("signon.rememberSignons", True)

            """Cookie Lifetime preferences
            0 The cookie's lifetime is supplied by the server. (Default)
            1 The user is prompted for the cookie's lifetime.
            2 The cookie expires at the end of the session (when the browser closes).
            3 The cookie lasts for the number of days specified by network.cookie.lifetime.days. (90 Days by default)"""
            profile.set_preference("network.cookie.lifetimePolicy", 3)
            
            """Cookie Behaviour preferences
            0 = accept all cookies by default
            1 = only accept from the originating site (block third party cookies)
            2 = block all cookies by default
            3 = use p3p settings (note: this is only applicable to older Mozilla Suite and Seamonkey versions.)
            4 = Storage access policy: Block cookies from trackers
            """
            profile.set_preference("network.cookie.cookieBehavior", 0)

            """ referer header preferences
            0 Never send the Referer header or set document.referrer.
            1 Send the Referer header when clicking on a link, and set document.referrer for the following page.
            2 Send the Referer header when clicking on a link or loading an image, and set document.referrer for the following page. (Default)"""
            profile.set_preference("network.http.sendRefererHeader", 2)

            """Javascript preferences"""
            profile.set_preference("javascript.enabled", True)

            """ Image Loading Preferences
            1 Allow all images to load, regardless of origin. (Default)
            2 Block all images from loading.
            3 Prevent third-party images from loading."""
            profile.set_preference("permissions.default.image", 1)

            """Opens a Browser to create the FirefoxProfile"""
            options = Options()
            options.headless = True
            browser = webdriver.Firefox(executable_path=self.geckopath, options=options, firefox_profile=profile)

            """save Path of Profile"""
            mozprofile = browser.capabilities["moz:profile"]
            print("moz:profile= ", mozprofile)
            
            """remove Lock so that the Profile can be copied"""
            try:
                os.remove(mozprofile + "/parent.lock")
            except:
                print('passed')
            print("lock removed")
            time.sleep(5)
            
            """saving the Profile as User x"""
            try:
                path = 'User__'+str(i)
                self.paths.append(path)
                shutil.copytree(mozprofile, path)
                print("profile copied")
            except:
                print('passed2')
            
            """quit Browser"""
            browser.quit()


if __name__ == "__main__":
    Profiles().create(5)
