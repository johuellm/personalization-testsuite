"""
Basic demo test on Dynamic Beghaviour of Websites based on Profiles
"""
import os
from scraping import Scraper
from analysis import AnalysisFunctions
from Profilecreation import Profiles
import time


class DemoTest1:
    """
    This is a demo test to determine whether a website shows Dynamic or whether
    it is a purely static website, by comparing hash results of the sourcecode
    and screenshots
    """

    def __init__(self, profiles=['User__1', 'User__2', 'User__3', 'User__4', 'User__5']):
        """
        :param profiles: path to the profiles (default is the output when running profilecreation.py)
        """
        self.profiles = profiles

    @staticmethod
    def delete_images(image_paths):
        """Deletion of Screenshots to clear the directory"""
        for path in image_paths:
            os.remove(path)

    def execute(self, url="http://127.0.0.1:5000/ecommerce"):
        """
        Method to start the test on a given url
        :param url: url of the website the test shall be executed on
        :return: Hashsimilarity of the source code and screenshots
        """
        sources = []
        image_paths = []
        for profile in self.profiles:
            scraper = Scraper(profile, headless=True)
            scraper.execute(url)
            sources.append(scraper.get_source())
            image_paths.append(scraper.get_imagepath())
            time.sleep(5)

        source_similarity = AnalysisFunctions.source_hashcomparison(sources)
        hash_image_similarity = AnalysisFunctions.image_hashcomparison(image_paths)
        self.delete_images(image_paths)

        print(f" The hash similarity of the extracted source codes is {source_similarity * 100 }% ")
        print( f" The hash similarity of the screenshots is {round(hash_image_similarity * 100 ,2)}% ")

        return source_similarity, hash_image_similarity


if "__main__" == __name__:
    DemoTest1().execute("http://127.0.0.1:5000/ecommerce/cols=4")
    DemoTest1().execute("http://127.0.0.1:5000/ecommerce/default=d")
    DemoTest1().execute("http://127.0.0.1:5000/ecommerce/default=p")
