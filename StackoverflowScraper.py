from Utils import *
from Job import *
from bs4 import BeautifulSoup as Soup
import urllib

class StackoverflowScraper(object):

    jobsFetched = []
    utils = Utils()

    '''
        Function to scrape Computer Science jobs from stackoverflow jobs portal
    '''
    def start(self, count):

        print '\nFetching jobs from stackoverflow jobs portal'

        webURL = "https://stackoverflow.com/jobs?sort=p&q=computer+science&l=san+jose"

        for page in range(1, 2):
            page = (page - 1) * 10
            url = "%s%d" % (webURL, page)
            target = Soup(urllib.urlopen(url), "html.parser")

            targetElements = target.findAll('div', attrs={'class': '-job-summary '})
            if targetElements == []:
                break
            for element in targetElements:
                # creating a job instance to store details like job title, company, address, JobLink
                job = Job()

                try:
                    title = element.find('a', attrs={'class': 'job-link'}).attrs['title']
                    if title != None:
                        job.jobTitle = title.strip()

                    company = element.find('div', attrs={'class': '-name'})
                    if company != None:
                        job.companyName = company.getText().strip()

                    addr = element.find('div', attrs={'class': '-location'})
                    if addr != None:
                        job.address = str(addr.getText().replace('-',' ').strip())

                    job.homeURL = "https://stackoverflow.com"
                    element = element.find('a', attrs={'class': 'job-link'}).attrs['href']
                    job.jobLink = "%s%s" % (job.homeURL, element)

                    if ((job.jobLink != "") and (job.jobLink != None)):
                        joburl = urllib.quote(job.jobLink.encode('utf8'), ':/')
                        joblinkTarget = Soup(urllib.urlopen(joburl), "html.parser")

                        summaryElement = joblinkTarget.find('div', attrs={'class': 'description'})
                        job.summary = self.utils.cleanAndProcess(summaryElement)

                    if (job.jobTitle != None and job.jobLink != None and job.summary != []):
                        self.jobsFetched.append(job)
                        job.id = count
                        count += 1
                        # job.printDetails()

                except Exception as e:
                    continue

        print "No. of jobs fetched: "+str(len(self.jobsFetched))
        print 'Fetching jobs from stackoverflow portal completed.'
        return self.jobsFetched