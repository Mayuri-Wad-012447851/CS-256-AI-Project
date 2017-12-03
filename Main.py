from Environment import *

'''
    Function which acts as a starting point to all services
'''
def main_run():

    env = Environment()

    # to iterate over options until a Quit signal is received
    while (True):

        print '\nWhat would you like to do?\n'

        print '1. Scrape jobs from web:\t'
        print '2. Cluster jobs (K-means and Single Link) \t'
        print '3. Quit'

        choice = raw_input("\nType your option : \t").strip()
        if choice == "3":
            exit(0)

        elif choice == "1":
            env.start_webscraping_jobs()

        elif choice == "2":
            env.initiate_clustering()

        else:
            print '\nYou entered values other than 1, 2 and 3. Please try again.'
            continue

if __name__ == '__main__':
    main_run()
