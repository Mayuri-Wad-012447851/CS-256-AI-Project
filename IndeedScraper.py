from Utils import *
from Job import *
from bs4 import BeautifulSoup as Soup
import urllib

class IndeedScraper(object):

    jobsFetched = []
    utils = Utils()
    '''
        Function to scrape Computer Science jobs from indeed.com
    '''
    def start(self, count):
        print '\nFetching jobs from indeed.com'

        urlKeyword = "Computer Science"
        webURL = "http://www.indeed.com/jobs?q=" + urlKeyword + "&start="

        for page in range(1, 2):
            page = (page - 1) * 10
            url = "%s%d" % (webURL, page)
            target = Soup(urllib.urlopen(url), "html.parser")

            targetElements = target.findAll('div', attrs={'class': ' row result'})
            if targetElements == []:
                break
            for element in targetElements:
                try:
                    # creating a job instance to store details like job title, company, address, JobLink
                    job = Job()

                    company = element.find('span', attrs={'class': 'company'})
                    if company != None:
                        job.companyName = company.getText().strip()
                    title = element.find('a', attrs={'class': 'turnstileLink'}).attrs['title']

                    if title != None:
                        job.jobTitle = title.strip()

                    addr = element.find('span', attrs={'class': 'location'})
                    if addr != None:
                        job.address = addr.getText().strip()

                    job.homeURL = "http://www.indeed.com"
                    job.jobLink = "%s%s" % (job.homeURL, element.find('a').get('href'))

                    skillsElement = element.find('span', attrs={'class': 'experienceList'})
                    job.skills = self.utils.clean_process_summary(skillsElement)

                    summaryElement = element.find('span', attrs={'class': 'summary'})
                    job.summary = self.utils.clean_process_summary(summaryElement)

                    if ((job.jobLink != "") and (job.jobLink != None)):
                        joburl = urllib.quote(job.jobLink.encode('utf8'), ':/')
                        joblinkTarget = Soup(urllib.urlopen(joburl), "html.parser")
                        summaryElement = joblinkTarget.find('span', attrs={'class': 'summary'})
                        job.summary.extend(self.utils.clean_process_summary(summaryElement))

                    if (job.jobTitle != None and job.jobLink != None):
                        self.jobsFetched.append(job)
                        job.id = count
                        count += 1
                        # job.printDetails()

                except Exception as e:
                    print e.message
                    continue

        print "No. of jobs fetched: " + str(len(self.jobsFetched))
        print 'Fetching jobs from indeed.com completed.'
        return self.jobsFetched