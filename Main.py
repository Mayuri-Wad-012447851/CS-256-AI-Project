from Webscraper import *
from Utils import *
import argparse


'''
    Function which acts as a starting point to all services
'''
def main_run(**kwargs):

    utils = Utils()

    # to iterate over options until a Quit signal is received
    while (True):

        print '\nWhat would you like to do?\n'

        print '1. Scrape jobs from web:\t'
        print '2. Cluster jobs using k-means\t'
        print '3. Cluster jobs using single link hierarchical clustering \t'
        print '4. Cluster jobs using complete link hierarchical clustering\t'
        print '5. Quit'

        choice = raw_input("\nType your option : \t").strip()
        if choice == "5":
            exit(0)

        elif choice == "1":

            scraper = Webscraper()
            # scraper.run_handshake_scraper(kwargs["username"],kwargs["password"])
            # scraper.run_glassdoor_scraper()
            scraper.run_dice_scraper()
            scraper.run_indeed_scraper()

        elif choice == "2":
            utils.process_data_for_clustering()


        elif choice == "3":
            pass

        elif choice == "4":
            pass

        else:
            print '\nYou entered values other than 1, 2, 3, 4, 5, 6, 7. Please try again.'
            continue

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="""
            parse parameters
            """)
    parser.add_argument('--username', type=str,
                        help="""
            enter username
            """)
    parser.add_argument('--password', type=str,
                        help="""
            enter password
            """)
    return vars(parser.parse_args())

if __name__ == '__main__':
    search_keys = parse_command_line_args()
    main_run(**search_keys)
