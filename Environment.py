from Webscraper import *
from SingleLinkClusteringAgent import *
from Utils import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

vectorizer = TfidfVectorizer(stop_words='english')

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

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(job_documents)
        model = KMeans(n_clusters=number_of_clusters, init='k-means++', max_iter=1000, n_init=1)
        model.fit_transform(X)

        # print "labels---------------------------"
        # print model.labels_
        #
        # print "cluster centers---------------------"
        # print model.cluster_centers_

        for i in range(len(model.labels_)):
            self.jobs_fetched[i].cluster = int(model.labels_[i])

        # for job in self.jobs_fetched:
        #     print job.jobTitle
        #     print job.cluster

        clusters = {}
        for i in range(number_of_clusters):
            clusters[i] = []

        for job in self.jobs_fetched:
            clusters[job.cluster].append(job)


        for k,v in clusters.items():
            print "Cluster"+str(k)+"---------------"
            for job in v:
                print "\t"+job.jobTitle

        while (True):
            try:
                number_of_clusters_for_nlp = raw_input("Enter number of top clusters to choose for NLP: ")
                number_of_clusters_for_nlp = int(number_of_clusters_for_nlp)
                break
            except:
                print "Invalid input. Please try again."

        print 'Printing 2 biggest clusters..'
        count = 0
        for k in sorted(clusters, key=lambda k: len(clusters[k]), reverse=True):
            count += 1
            print "Cluster" + str(k) + "---------------"
            for job in clusters[k]:
                print "\t" + job.jobTitle

            print 'Initiating single-link hierarchical clustering on Cluster '+str(k)
            single_link_clustering_agent = SingleLinkClusteringAgent()

            single_link_clustering_agent.start(clusters[k])

            if count == number_of_clusters_for_nlp:
                break











