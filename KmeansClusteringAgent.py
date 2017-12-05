from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

vectorizer = TfidfVectorizer(stop_words='english')

class KmeansClusteringAgent:


    def __init__(self, jobs_fetched):
        self.jobs_fetched = jobs_fetched

    def start(self, job_documents, number_of_clusters):
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

        for k, v in clusters.items():
            print "Cluster" + str(k) + "---------------"
            for job in v:
                print "\t" + job.jobTitle

        return clusters