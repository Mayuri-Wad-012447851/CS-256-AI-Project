'''
Class Webscraper acts as an interface or parent class to 3 webscraper modules
Author : Mayuri Wadkar
'''

from DiceScraper import *
from IndeedScraper import *
from StackoverflowScraper import *

class Webscraper(object):

    jobs_fetched = []

    '''
        Function which initiates crawler on stackoverflow job portal
        It stores fetched jobs in jobs_fetched array
    '''
    def run_stackoverflow_scraper(self):
        scraper = StackoverflowScraper()
        jobs = scraper.start(len(self.jobs_fetched))
        self.jobs_fetched.extend(jobs)

    '''
        Function which initiates crawler on dice.com
        It stores fetched jobs in jobs_fetched array
    '''
    def run_dice_scraper(self):
        scraper = DiceScraper()
        jobs = scraper.start(len(self.jobs_fetched))
        self.jobs_fetched.extend(jobs)

    '''
        Function which initiates crawler on indeed.com
        It stores fetched jobs in jobs_fetched array
    '''
    def run_indeed_scraper(self):
        scraper = IndeedScraper()
        jobs = scraper.start(len(self.jobs_fetched))
        self.jobs_fetched.extend(jobs)