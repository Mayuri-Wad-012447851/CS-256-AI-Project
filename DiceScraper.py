from bs4 import BeautifulSoup as Soup
import urllib
from Job import *

class DiceScraper(object):

    def __init__(self):
        pass

    def start(self):

        webURL = "https://www.dice.com/jobs?q=Computer+Science&l=San+Jose%2C+CA"
        for page in range(1, 101):
            page = (page - 1) * 10
            url = "%s%d" % (webURL, page)
            target = Soup(urllib.urlopen(url), "html.parser")

            targetElements = target.findAll('div', attrs={'class': ' row result'})
            if targetElements == []:
                break
            for element in targetElements:
                # creating a job instance to store details like job title, company, address, JobLink
                job = Job()

                company = element.find('span', attrs={'itemprop': 'name'})
                if company != None:
                    job.companyName = company.getText().strip()
                title = element.find('a', attrs={'class': 'turnstileLink'}).attrs['title']
                if title != None:
                    job.jobTitle = title.strip()
                addr = element.find('span', attrs={'itemprop': 'addressLocality'})
                if addr != None:
                    job.address = addr.getText().strip()
                job.homeURL = "http://www.indeed.com"
                job.jobLink = "%s%s" % (job.homeURL, element.find('a').get('href'))

                skillsElement = element.find('span', attrs={'class': 'experienceList'})
                job.skills = self.cleanAndProcess(skillsElement)

                summaryElement = element.find('span', attrs={'class': 'summary'})
                job.summary = self.cleanAndProcess(summaryElement)

                if (job.jobTitle != None and job.jobLink != None):
                    self.jobsFetched.append(job)