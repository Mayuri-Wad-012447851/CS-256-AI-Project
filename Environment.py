from Webscraper import *
from SingleLinkClusteringAgent import *
from Utils import *
from KmeansClusteringAgent import *
from Topic import *


class Environment:

    utils = Utils()
    jobs_fetched = []

    def start_webscraping_jobs(self):

        scraper = Webscraper()
        scraper.run_stackoverflow_scraper()
        scraper.run_dice_scraper()
        scraper.run_indeed_scraper()
        self.jobs_fetched = Webscraper.jobs_fetched


    def initiate_clustering(self):

        while(True):
            try:
                number_of_clusters = raw_input("Enter number of clusters: ")
                number_of_clusters = int(number_of_clusters)
                break
            except:
                print "Invalid input. Please try again."

        job_documents = []

        for job in self.jobs_fetched:
            desc = " ".join(job.summary)
            job_documents.append(desc)

        # for doc in job_documents:
        #     print doc+"\n\n"

        kmeans = KmeansClusteringAgent(self.jobs_fetched)
        clusters = kmeans.start(job_documents, number_of_clusters)

        while (True):
            try:
                number_of_clusters_for_nlp = raw_input("Enter number of top clusters to choose for NLP: ")
                number_of_clusters_for_nlp = int(number_of_clusters_for_nlp)
                break
            except:
                print "Invalid input. Please try again."

        print 'Below are '+str(number_of_clusters_for_nlp)+' biggest clusters of all clusters built using Kmeans'
        final_clusters_for_nlp = {}
        topics = []
        count = 0
        for k in sorted(clusters, key=lambda k: len(clusters[k]), reverse=True):
            count += 1
            print "Cluster" + str(k) + "---------------"


            final_clusters_for_nlp[k] = clusters[k]

            for job in clusters[k]:
                print "\t" + job.jobTitle

            print 'Initiating single-link hierarchical clustering on Cluster '+str(k)
            single_link_clustering_agent = SingleLinkClusteringAgent()

            topic_name = single_link_clustering_agent.start(clusters[k])

            #for now setting it to default dummy name
            topic_name = "Cluster" + str(k)

            topic = Topic(topic_name)
            topic.set_syllabus_content(clusters[k])
            topics.append(topic)

            if count == number_of_clusters_for_nlp:
                break

        for topic in topics:
            print topic.topic_name
            print topic.s















