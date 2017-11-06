from GlassdoorScraper import *
from HandshakeScraper import *
from DiceScraper import *
from IndeedScraper import *

class Webscraper(object):

    def run_handshake_scraper(self, username, password):
        scraper = HandshakeScraper(username, password)
        scraper.start()

    def run_glassdoor_scraper(self):
        scraper = GlassdoorScraper()
        scraper.start()

    def run_dice_scraper(self):
        scraper = DiceScraper()
        scraper.start()

    def run_indeed_scraper(self):
        scraper = IndeedScraper()
        scraper.start()