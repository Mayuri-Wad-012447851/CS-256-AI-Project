from Webscraper import *
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import numpy as np

vectorizer = TfidfVectorizer(stop_words='english')

class Environment:

    jobs_fetched = []

    def __init__(self):
        pass

    def process_summary(self, raw_summary):
        summary = raw_summary


        return summary

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

        for k,v in tf_matrix.items():
            print str(k) + " : \t\t" + str(v)

        idf_terms = {}
        for term in terms:
            termVector = Corpus[term]
            occurance = 0
            for k in range(0, len(termVector)):
                if termVector[k] != 0:
                    occurance += 1
            idf_terms[term] = math.log(float(len(self.jobs_fetched) / occurance))

        for k,v in idf_terms.items():
            print str(k) + " : \t\t" + str(v)


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

        print 'Clustering job documents..'
        job_documents = []

        for job in self.jobs_fetched:
            job_documents.append(' '.join(job.summary))

        X = vectorizer.fit_transform(job_documents)

        true_k = 2
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=1000, n_init=1)
        model.fit(X)

        print("Top terms per cluster:")
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        for i in range(true_k):
            print("Cluster %d:" % i),
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind])





