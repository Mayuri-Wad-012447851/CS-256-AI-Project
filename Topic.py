'''
Topic class to simulate course topic
Author : Mayuri Wadkar
'''

from Utils import technologies_stopwords, fetch_description_techs
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

    '''
    Function to initiate extraction of course topic, technologies, action lists and summary
    '''
    def set_syllabus_content(self):

        job_closest_to_centroid = self.cluster.closest_job_document
        description_of_job_closest_to_centroid, techSet_of_job_closest_to_centroid = fetch_description_techs(job_closest_to_centroid.jobLink)
        title_of_job_closest_to_centroid = job_closest_to_centroid.jobTitle

        #integration with NLP
        job_descriptions = ""
        # job_titles = ""
        technologies = set()

        for job in self.cluster.cluster:
            url = job.jobLink
            # print job.jobLink
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
            # job_titles += job.jobTitle

        summarizer = SummarizationModule()

        self.summary = summarizer.summarize_job_descriptions(job_descriptions)
        self.listedTech, self.actionList = summarizer.get_listed_tech_and_action_list(job_descriptions)
        self.technologies = technologies
        self.topic = summarizer.get_topic(title_of_job_closest_to_centroid)