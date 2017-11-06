from GlassdoorScraper import *
from HandshakeScraper import *
from DiceScraper import *
from IndeedScraper import *

class Webscraper(object):

    jobs_fetched = []

    def run_handshake_scraper(self, username, password):
        scraper = HandshakeScraper(username, password)
        self.jobs_fetched.extend(scraper.start())

    def run_glassdoor_scraper(self):
        scraper = GlassdoorScraper()
        self.jobs_fetched.extend(scraper.start())

    def run_dice_scraper(self):
        scraper = DiceScraper()
        self.jobs_fetched.extend(scraper.start())

    def run_indeed_scraper(self):
        scraper = IndeedScraper()
        self.jobs_fetched.extend(scraper.start())