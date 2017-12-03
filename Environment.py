from Webscraper import *
from Utils import *
from SingleLinkClusteringAgent import *
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import numpy as np
from random import randint
import operator

vectorizer = TfidfVectorizer(stop_words='english')

class Environment:

    utils = Utils()
    jobs_fetched = []

    def start_webscraping_jobs(self):

        scraper = Webscraper()
        # scraper.run_handshake_scraper(kwargs["username"],kwargs["password"])
        scraper.run_stackoverflow_scraper()
        scraper.run_dice_scraper()
        scraper.run_indeed_scraper()
        self.jobs_fetched = Webscraper.jobs_fetched


    def compute_vectors(self):

        Corpus = {}

        for job in self.jobs_fetched:
            for word in job.summary:
                if word not in Corpus.keys():
                    frequencies = []
                    for i in range(0, len(self.jobs_fetched)):
                        frequencies.append(0)
                    Corpus[word] = frequencies
                    Corpus[word][job.id] = 1
                Corpus[word][job.id] += 1

        # for k,v in Corpus.items():
        #     print str(k)+" : \t\t"+str(v)

        tf_matrix = {}

        terms = Corpus.keys()

        # reversing the corpus
        for job in self.jobs_fetched:
            array_termFrequency = []
            for k in range(0, len(terms)):
                array_termFrequency.append(0)
            tf_matrix[job.id] = array_termFrequency

        for job in self.jobs_fetched:
            for j in range(0, len(terms)):
                word = terms[j]
                tf_matrix[job.id][j] = Corpus[word][job.id]

        # for k,v in tf_matrix.items():
        #     print str(k) + " : \t\t" + str(v)

        idf_terms = {}
        for term in terms:
            termVector = Corpus[term]
            occurance = 0
            for k in range(0, len(termVector)):
                if termVector[k] != 0:
                    occurance += 1
            idf_terms[term] = math.log(float(len(self.jobs_fetched) / occurance))

        # for k,v in idf_terms.items():
        #     print str(k) + " : \t\t" + str(v)


        for job in self.jobs_fetched:
            termFreq = tf_matrix[job.id]
            # finding TF for each job document
            for k in range(0, len(termFreq)):
                var1 = termFreq[k]
                var2 = sum(tf_matrix[job.id])
                job.TFvector.append((float(var1) / float(var2)))
            print str(job.id) + " :" + str(job.TFvector)

        # computing TF*IDF for every job document
        for job in self.jobs_fetched:
            for i in range(0, len(terms)):
                val = idf_terms[terms[i]]
                val2 = job.TFvector[i]
                job.TF_IDF.append(float(val) * float(val2))

            print str(job.id) + " :" + str(job.TF_IDF)

        # for job in self.jobs_fetched:
        #     print job.jobTitle
        #     print " ".join(job.summary)
        #     print "\n"


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
            if count == number_of_clusters_for_nlp:
                break

            print 'Initiating single-link hierarchical clustering on Cluster '+str(k)
            single_link_clustering_agent = SingleLinkClusteringAgent()

            single_link_clustering_agent.start(clusters[k])











