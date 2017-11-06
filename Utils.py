from Webscraper import *

class Utils(object):
    TF_Corpus = {}
    TF_Reversed_Corpus = {}
    term_IDFs = {}

    #This method builds a job document term matrix
    def buildCorpus(self):
        Corpus = {}
        ReversedCorpus = {}

        for job in Webscraper.jobs_fetched:
            for word in job.summary:
                if word not in Corpus.keys():
                    frequencies = []
                    for i in range(0, len(Webscraper.jobs_fetched)):
                        frequencies.append(0)
                    Corpus[word] = frequencies
                Corpus[word][job.id] += 1

        terms = Corpus.keys()

        # reversing the corpus
        for i in range(0, len(Webscraper.jobs_fetched)):
            array_termFrequency = []
            for k in range(0, len(terms)):
                array_termFrequency.append(0)
            ReversedCorpus[i] = array_termFrequency

        jobIDs = ReversedCorpus.keys()

        for jobIdkey in jobIDs:
            for j in range(0, len(terms)):
                word = terms[j]
                ReversedCorpus[jobIdkey][j] = Corpus[word][jobIdkey]

        for job in Webscraper.jobs_fetched:
            termFreq = ReversedCorpus[job.id]
            # finding TF for each job document
            for k in range(0, len(termFreq)):
                var1 = termFreq[k]
                var2 = sum(ReversedCorpus[job.id])
                job.TFvector.append(float(var1 / var2))

        #calculating IDFs of all terms
        idf_terms = {}
        for term in terms:
            termVector = Corpus[term]
            occurance = 0
            for k in range(0,len(termVector)):
                if termVector[k] != 0:
                    occurance += 1
            idf_terms[term] = math.log(float(len(jobIDs) / occurance))

        #computing TF*IDF for every job document
        for job in Webscraper.jobs_fetched:
            for i in range(0,len(terms)):
                val = float(idf_terms[terms[i]])
                val2 = float(job.TFvector[i])
                job.TF_IDF.append(float(val * val2))

        self.TF_Corpus = Corpus
        self.TF_Reversed_Corpus = ReversedCorpus
        self.term_IDFs = idf_terms

    #This method normalizes term frequency job document
    def normalizePercept(self, vector):
        factor = 0
        NormalizedVector = []

        for val in vector:
            factor += val
        for val in vector:
            NormalizedVector.append(float(val/factor))

        terms = self.TF_Corpus.keys()
        perceptIDF = []
        for i in range(0,len(vector)):
            perceptIDF.append(float(NormalizedVector[i]*self.term_IDFs[str(terms[i])]))

        return perceptIDF