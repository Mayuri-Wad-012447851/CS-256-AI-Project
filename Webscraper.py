from GlassdoorScraper import *
from HandshakeScraper import *
from DiceScraper import *
from IndeedScraper import *

class Webscraper(object):

    jobs_fetched = []

    '''
        Function which initiates crawler on handshake portal
        It stores fetched jobs in jobs_fetched array
    '''
    def run_handshake_scraper(self, username, password):
        scraper = HandshakeScraper(username, password)
        self.jobs_fetched.extend(scraper.start())

    '''
        Function which initiates crawler on glassdoor portal
        It stores fetched jobs in jobs_fetched array
    '''
    def run_glassdoor_scraper(self):
        scraper = GlassdoorScraper()
        self.jobs_fetched.extend(scraper.start())

    '''
        Function which initiates crawler on dice.com
        It stores fetched jobs in jobs_fetched array
    '''
    def run_dice_scraper(self):
        scraper = DiceScraper()
        self.jobs_fetched.extend(scraper.start())

    '''
        Function which initiates crawler on indeed.com
        It stores fetched jobs in jobs_fetched array
    '''
    def run_indeed_scraper(self):
        scraper = IndeedScraper()
        self.jobs_fetched.extend(scraper.start())