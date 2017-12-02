from bs4 import BeautifulSoup as Soup
from Job import *
import re, urllib
from Utils import *

class DiceScraper(object):

    jobsFetched = []
    utils = Utils()


    '''
        Function to scrape Computer Science jobs from dice.com
    '''
    def start(self, count):

        print '\nFetching jobs from dice.com'

        webURL = "https://www.dice.com/jobs?q=Computer+Science&l=San+Jose%2C+CA"

        for page in range(1, 2):
            page = (page - 1) * 10
            url = "%s%d" % (webURL, page)
            target = Soup(urllib.urlopen(url), "html.parser")

            targetElements = target.findAll('div', attrs={'class': 'complete-serp-result-div'})
            if targetElements == []:
                break
            for element in targetElements:
                # creating a job instance to store details like job title, company, address, JobLink
                job = Job()

                title = element.find('span', attrs={'itemprop': 'title'})
                if title != None:
                    job.jobTitle = title.getText().strip()

                company = element.find('span', attrs={'class': 'compName'})
                if company != None:
                    job.companyName = company.getText().strip()

                addr = element.find('span', attrs={'class': 'jobLoc'})
                if addr != None:
                    job.address = addr.getText().strip()

                job.homeURL = "https://www.dice.com"
                sub = element.find('a', attrs={'itemprop': 'url'}).attrs['href']
                job.jobLink = "%s%s" % (job.homeURL, sub)

                if ((job.jobLink != "") and (job.jobLink != None)):
                    # joburl = urllib.quote(job.jobLink.encode('utf8'), ':/')
                    joblinkTarget = Soup(urllib.urlopen(job.jobLink), "html.parser")


                    summaryElement = joblinkTarget.find('div', attrs={'itemprop': 'description'})
                    job.summary = self.utils.cleanAndProcess(summaryElement)

                if (job.jobTitle != None and job.jobLink != None and job.summary != []):
                    self.jobsFetched.append(job)
                    job.id = count
                    count += 1
                    # job.printDetails()

        print "No. of jobs fetched: " + str(len(self.jobsFetched))
        print 'Fetching jobs from dice.com completed.'
        return self.jobsFetched

