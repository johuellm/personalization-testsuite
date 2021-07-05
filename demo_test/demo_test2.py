"""
Basic demo test on Personalization of Websites based on Profiles
"""

import os
from demo_test.scraping import Scraper
from demo_test.analysis import AnalysisFunctions
from demo_test.Profilecreation import Profiles
import time
from timeit import timeit


class DemoTest2:
    """
    This is a demo test to determine if a website is personalized or not
    ()
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
        # Collection variables
        intra_source_similarities = []
        intra_image_similarities = []
        sources = []
        image_paths = []

        for profile in self.profiles:
            # Scraping for Data 1
            scraper1 = Scraper(profile, headless=True)
            scraper1.execute(url)
            source1 = scraper1.get_source()
            sources.append(source1)
            image_path1 = scraper1.get_imagepath()
            image_paths.append(image_path1)
            time.sleep(5)

            # Scraping for Data 2
            scraper2 = Scraper(profile, headless=True)
            scraper2.execute(url)
            source2 = scraper2.get_source()
            image_path2 = scraper2.get_imagepath()

            # calculate the intra profile similarities
            intra_image_similarities.append(AnalysisFunctions.image_hashcomparison([image_path1, image_path2]))
            intra_source_similarities.append(AnalysisFunctions.source_hashcomparison([source1, source2]))

            #deleted th image path that is not used anymore
            self.delete_images([image_path2])

        # Intra Profile Comparison
        intra_source_similarity = sum(intra_source_similarities)/len(intra_source_similarities)
        intra_image_similaritiy = sum(intra_image_similarities)/len(intra_image_similarities)


        # Inter Profile Comparison
        source_similarity = AnalysisFunctions.source_hashcomparison(sources)
        image_similarity = AnalysisFunctions.image_hashcomparison(image_paths)

        self.delete_images(image_paths)
        print(f" The Similarities when comparing intra profile are {intra_source_similarity * 100}% and {intra_image_similaritiy * 100}%")
        print(f" The Similarities when comparing inter profile are {source_similarity * 100}% and {image_similarity * 100}%")

        # decide on personalization
        if intra_image_similaritiy > image_similarity and intra_source_similarity > source_similarity:
            personalization = True
        else:
            personalization = False
        return personalization


if "__main__" == __name__:
    print("STATIC:")
    print(DemoTest2().execute("http://127.0.0.1:5000/ecommerce"))
    print("DYNAMIC:")
    print(DemoTest2().execute("http://127.0.0.1:5000/ecommerce/default=d"))
    print("PERSONALIZED")
    print(DemoTest2().execute("http://127.0.0.1:5000/ecommerce/default=p"))
