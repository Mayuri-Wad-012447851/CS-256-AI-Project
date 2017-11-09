from HandshakeScraper import *
from DiceScraper import *
from IndeedScraper import *
from StackoverflowScraper import *

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
        Function which initiates crawler on stackoverflow job portal
        It stores fetched jobs in jobs_fetched array
    '''
    def run_stackoverflow_scraper(self):
        scraper = StackoverflowScraper()
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