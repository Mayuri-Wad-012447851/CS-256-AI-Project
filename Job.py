'''
Job class to simulate job fetched from web
Author : Mayuri Wadkar
'''

import urllib

class Job:

    #initializing all job features
    def __init__(self):
        self.id = None
        self.jobTitle = None
        self.companyName = None
        self.address = None
        self.homeURL = None
        self.jobLink = None
        self.skills = []
        self.summary = []
        self.TFvector = []
        self.TF_IDF = []
        self.cluster = None

    #method to print job features
    def printDetails(self):
        print "Job ID:\t"+str(self.id)
        print "Job Title:\t"+str(self.jobTitle.encode('ascii', 'ignore'))
        print "Location:\t" + str(self.address)
        print "Company:\t"+str(self.companyName)
        joburl = urllib.quote(self.jobLink.encode('utf8'), ':/')
        print "Link:\t"+str(joburl)
        # print str(self.summary)


