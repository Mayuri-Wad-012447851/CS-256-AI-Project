
from Utils import technologies_stopwords
from SummarizationModule import *
from bs4 import BeautifulSoup as Soup
import urllib

class Topic:

    def __init__(self):
        self.cluster = None
        self.topic = None
        self.technologies = None
        self.listedTech = None
        self.actionList = None
        self.summary = None

    def set_syllabus_content(self):


        #integration with NLP
        job_descriptions = ""
        technologies = set()

        for job in self.cluster:
            url = job.jobLink
            print job.jobLink
            joblinkTarget = Soup(urllib.urlopen(url), "html.parser")
            techTags = joblinkTarget.findAll('a', attrs={'class': 'post-tag job-link no-tag-menu'})
            for tag in range(len(techTags)):
                tech = str(techTags[tag].get_text())
                if tech not in technologies_stopwords:
                    technologies.add(tech)

            job_description = joblinkTarget.find('div', attrs={'class': 'description'})
            if job_description != None:
                job_description = job_description.get_text()
            else:
                job_description = joblinkTarget.find('span', attrs={'class': 'summary'})
                if job_description != None:
                    job_description = job_description.get_text()
                else:
                    job_description = joblinkTarget.find('div', attrs={'itemprop': 'description'})
                    if job_description != None:
                        job_description = job_description.get_text()
            if job_description != None:
                job_descriptions += job_description

        summarizer = SummarizationModule()

        self.summary = summarizer.summarize_job_descriptions(job_descriptions)
        self.listedTech, self.actionList = summarizer.get_listed_tech_and_action_list(job_descriptions)
        self.technologies = technologies
        self.topic = summarizer.get_topic(job_descriptions)