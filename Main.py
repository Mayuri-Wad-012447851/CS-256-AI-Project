from Environment import *
from Utils import *
import argparse


'''
    Function which acts as a starting point to all services
'''
def main_run(**kwargs):

    utils = Utils()
    env = Environment()

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
            env.start_webscraping_jobs()

        elif choice == "2":
            env.initiate_clustering()

        elif choice == "3":
            utils.process_data_for_clustering()
            # create seperate .py file for single link clustering mode
            # call clustering function here

        elif choice == "4":
            utils.process_data_for_clustering()
            # create seperate .py file for complete link clustering mode
            # call clustering function here

        else:
            print '\nYou entered values other than 1, 2, 3, 4, 5. Please try again.'
            continue

'''
    Function to parse command line arguments required for handshake scraper
    It parses input username and password for handshake login
'''
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
