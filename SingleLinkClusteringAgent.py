from Utils import *
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class SingleLinkClusteringAgent:

    utils = Utils()

    def start(self, jobs):

        # topic_name = ""
        #
        # Corpus = {}
        #
        # #corpus generation..
        # # it generates a dictionary with keys as words from descriptions and values are their frequencies in job documents
        # for i in range(len(jobs)):
        #     job = jobs[i]
        #     for word in job.summary:
        #         if word not in Corpus.keys():
        #             frequencies = []
        #             for k in range(len(jobs)):
        #                 frequencies.append(0)
        #             Corpus[word] = frequencies
        #             Corpus[word][i] = 1
        #         Corpus[word][i] += 1
        #
        # # print "===============Corpus=========="
        # # for k,v in Corpus.items():
        # #     print str(k)+" : \t\t"+str(v)
        #
        # #steps to generate term frequency matrix
        # tf_matrix = {}
        #
        # terms = Corpus.keys()
        #
        # # reversing the corpus
        # for i in range(len(jobs)):
        #     array_termFrequency = []
        #     for k in range(0, len(terms)):
        #         array_termFrequency.append(0)
        #     tf_matrix[i] = array_termFrequency
        #
        # for i in range(len(jobs)):
        #     for j in range(len(terms)):
        #         word = terms[j]
        #         tf_matrix[i][j] = Corpus[word][i]
        #
        # # print "\n==================TF Matrix====================="
        # # for k,v in tf_matrix.items():
        # #     print str(k) + " : \t\t" + str(v)
        #
        # #steps to compute IDFs for all words in corpus
        # idf_terms = {}
        # for term in terms:
        #     termVector = Corpus[term]
        #     occurance = 0
        #     for k in range(0, len(termVector)):
        #         if termVector[k] != 0:
        #             occurance += 1
        #     idf_terms[term] = math.log(float(len(jobs) / occurance))
        #
        # # print "\n================TERM_IDFs======================="
        # # for k,v in idf_terms.items():
        # #     print str(k) + " : \t\t" + str(v)
        #
        # #computing TFs for all job documents
        # for i in range(len(jobs)):
        #     termFreq = tf_matrix[i]
        #     # finding TF for each job document
        #     for k in range(0, len(termFreq)):
        #         var1 = termFreq[k]
        #         var2 = sum(tf_matrix[i])
        #
        #         jobs[i].TFvector.append((float(var1) / float(var2)))
        #     # print str(i)+" -- "+str(jobs[i].id) + " :" + str(jobs[i].TFvector)
        #
        # # computing TF*IDF for every job document
        # for k in range(len(jobs)):
        #     for i in range(0, len(terms)):
        #         val = idf_terms[terms[i]]
        #         val2 = jobs[k].TFvector[i]
        #         jobs[k].TF_IDF.append(float(val) * float(val2))
        #
        #     # print str(k)+" -- "+str(jobs[k].id) + " :" + str(jobs[k].TF_IDF)
        #
        # # generating distance matrix for all job documents using cosine distance
        #
        # distance_matrix = {}
        # for i in range(len(jobs)):
        #     distance_matrix[i] = []
        #     for j in range(len(jobs)):
        #         if i != j:
        #             distance_matrix[i].append(self.utils.cosine_distance(jobs[i].TF_IDF, jobs[j].TF_IDF))
        #         else:
        #             distance_matrix[i].append(0)
        # # print '=============Distance Matrix=================='
        # #
        # # for k, v in distance_matrix.items():
        # #     print str(k)+" : "+str(v)
        #

        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')

        tf = tf_vectorizer.fit_transform(job_documents)
        lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)

        lda.fit(tf)

        print("\nTopics in LDA model:")
        tf_feature_names = tf_vectorizer.get_feature_names()
        print_top_words(lda, tf_feature_names, n_top_words)

        #goal
        return topic_name
