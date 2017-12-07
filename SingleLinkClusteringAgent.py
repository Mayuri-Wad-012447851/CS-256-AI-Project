'''
SingleLinkClusteringAgent class to perform single link hierarchical clustering on array of job descriptions
Author : Pratik Surana
'''

from Utils import fetch_description_techs
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import single, dendrogram, leaves_list

class SingleLinkClusteringAgent:

    cluster = None

    def start(self):

        job_descriptions = []
        titles = []
        for job in self.cluster.cluster:
            job_url = job.jobLink
            job_description, techs = fetch_description_techs(job_url)
            if job_description == "" or job_description == None:
                job_descriptions.append(job.jobTitle)
            else:
                job_descriptions.append(job_description)
            titles.append(job.jobTitle)

        vectorizer = CountVectorizer(input='job_descriptions')
        dtm = vectorizer.fit_transform(job_descriptions)
        vocab = vectorizer.get_feature_names()

        dtm = dtm.toarray()
        vocab = np.array(vocab)
        dist = 1 - cosine_similarity(dtm)
        np.round(dist, 2)

        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
        pos = mds.fit_transform(dist)

        linkage_matrix = single(dist)
        dendrogram(linkage_matrix, orientation="right", labels=titles)
        leaves = leaves_list(linkage_matrix)
        plt.subplots_adjust(left=0.50)
        parent_job = self.cluster.cluster[leaves[0]]
        plt.savefig('./Plots/Cluster_'+str(self.cluster.cluster_id)+'_SingleLinkClusteringPlot.png')
        # plt.show()
        return parent_job



