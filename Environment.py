from Webscraper import *

class Environment:

    jobs_fetched = []

    def __init__(self):
        pass

    def start_webscraping_jobs(self):

        scraper = Webscraper()
        # scraper.run_handshake_scraper(kwargs["username"],kwargs["password"])
        scraper.run_stackoverflow_scraper()
        scraper.run_dice_scraper()
        scraper.run_indeed_scraper()
        self.jobs_fetched = Webscraper.jobs_fetched

    def initiate_clustering(self):

        while (True):
            print '1. Cluster using pre-fetched and pre-computed data.'
            print '2. Scrape new data and cluster'
            print '3. Return to main menu'
            print 'Enter option:\t'

            choice = raw_input("\nType your option : \t").strip()
            if choice == "3":
                return

            if choice == "1":
                pass

            if choice == "2":
                pass

            else:
                print '\nYou entered values other than 1, 2, 3, 4, 5. Please try again.'
                continue
