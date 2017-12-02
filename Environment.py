from Webscraper import *
from Utils import *
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


    def initiate_clustering(self):

        job_documents = []

        clusters = 3

        for job in self.jobs_fetched:
            desc = " ".join(job.summary)
            job_documents.append(desc)

        # for doc in job_documents:
        #     print doc+"\n\n"

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(job_documents)
        model = KMeans(n_clusters=clusters, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)

        # print "labels---------------------------"
        # print model.labels_
        #
        # print "cluster centers---------------------"
        # print model.cluster_centers_

        for i in range(len(model.labels_)):
            self.jobs_fetched[i].cluster = int(model.labels_[i])

        cluster0 = []
        cluster1 = []
        cluster2 = []

        for job in self.jobs_fetched:
            if job.cluster == 0:
                cluster0.append(job)
            elif job.cluster == 1:
                cluster1.append(job)
            elif job.cluster == 2:
                cluster2.append(job)

        print 'Cluster 0:\n--------------------'
        for job in cluster0:
            print job.jobTitle

        print 'Cluster 1:\n--------------------'
        for job in cluster1:
            print job.jobTitle

        print 'Cluster 2:\n--------------------'
        for job in cluster2:
            print job.jobTitle







