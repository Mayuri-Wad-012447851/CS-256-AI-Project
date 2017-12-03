import math
from Utils import *

class SingleLinkClusteringAgent:

    utils = Utils()

    def start(self, jobs):

        for job in jobs:
            print job.id
            print job.jobTitle
            print job.summary

        Corpus = {}

        for i in range(len(jobs)):
            job = jobs[i]
            for word in job.summary:
                if word not in Corpus.keys():
                    frequencies = []
                    for k in range(len(jobs)):
                        frequencies.append(0)
                    Corpus[word] = frequencies
                    Corpus[word][i] = 1
                Corpus[word][i] += 1

        print "===============Corpus=========="
        for k,v in Corpus.items():
            print str(k)+" : \t\t"+str(v)

        tf_matrix = {}

        terms = Corpus.keys()

        # reversing the corpus
        for i in range(len(jobs)):
            array_termFrequency = []
            for k in range(0, len(terms)):
                array_termFrequency.append(0)
            tf_matrix[i] = array_termFrequency

        for i in range(len(jobs)):
            for j in range(len(terms)):
                word = terms[j]
                tf_matrix[i][j] = Corpus[word][i]

        print "\n==================TF Matrix====================="
        for k,v in tf_matrix.items():
            print str(k) + " : \t\t" + str(v)

        idf_terms = {}
        for term in terms:
            termVector = Corpus[term]
            occurance = 0
            for k in range(0, len(termVector)):
                if termVector[k] != 0:
                    occurance += 1
            idf_terms[term] = math.log(float(len(jobs) / occurance))

        print "\n================TERM_IDFs======================="
        for k,v in idf_terms.items():
            print str(k) + " : \t\t" + str(v)

        for i in range(len(jobs)):
            termFreq = tf_matrix[i]
            # finding TF for each job document
            for k in range(0, len(termFreq)):
                var1 = termFreq[k]
                var2 = sum(tf_matrix[i])

                jobs[i].TFvector.append((float(var1) / float(var2)))
            print str(i)+" -- "+str(jobs[i].id) + " :" + str(jobs[i].TFvector)

        # computing TF*IDF for every job document
        for k in range(len(jobs)):
            for i in range(0, len(terms)):
                val = idf_terms[terms[i]]
                val2 = jobs[k].TFvector[i]
                jobs[k].TF_IDF.append(float(val) * float(val2))

            print str(k)+" -- "+str(jobs[k].id) + " :" + str(jobs[k].TF_IDF)

        # generating distance matrix for all job documents using cosine distance

        distance_matrix = {}
        for i in range(len(jobs)):
            distance_matrix[i] = []
            for j in range(len(jobs)):
                distance_matrix[i].append(self.utils.cosineDistance(jobs[i].TF_IDF, jobs[j].TF_IDF))

        print '=============Distance Matrix=================='

        for k, v in distance_matrix.items():
            print str(k)+" : "+str(v)
