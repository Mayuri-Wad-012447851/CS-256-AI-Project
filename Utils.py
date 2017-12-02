from Webscraper import *
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
stopWords = set(stopwords.words('english'))
stopWords.update(('a', "a's", 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after',
                     'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost', 'alone', 'along',
                     'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any',
                     'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear',
                     'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside', 'ask', 'asking',
                     'associated', 'at', 'available', 'away', 'awfully', 'b', 'be', 'became', 'because', 'become',
                     'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below',
                     'beside', 'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by', 'c',
                     "c'mon", "c's", 'came', 'can', "can't", 'cannot', 'cant', 'cause', 'causes', 'certain',
                     'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently',
                     'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could',
                     "couldn't", 'course', 'currently', 'd', 'definitely', 'described', 'despite', 'did', "didn't",
                     'different', 'do', 'does', "doesn't", 'doing', "don't", 'done', 'down', 'downwards', 'during', 'e',
                     'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough', 'entirely', 'especially',
                     'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex',
                     'exactly', 'example', 'except', 'f', 'far', 'few', 'fifth', 'first', 'five', 'followed',
                     'following', 'follows', 'for', 'former', 'formerly', 'forth', 'four', 'from', 'further',
                     'furthermore', 'g', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone',
                     'got', 'gotten', 'greetings', 'h', 'had', "hadn't", 'happens', 'hardly', 'has', "hasn't", 'have',
                     "haven't", 'having', 'he', "he's", 'hello', 'help', 'hence', 'her', 'here', "here's", 'hereafter',
                     'hereby', 'herein', 'hereupon', 'hers', 'herself', 'hi', 'him', 'himself', 'his', 'hither',
                     'hopefully', 'how', 'howbeit', 'however', 'i', "i'd", "i'll", "i'm", "i've", 'ie', 'if', 'ignored',
                     'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'inner',
                     'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it', "it'd", "it'll", "it's", 'its',
                     'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'knows', 'known', 'l', 'last',
                     'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's", 'like', 'liked',
                     'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'm', 'mainly', 'many', 'may', 'maybe', 'me',
                     'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much', 'must', 'my',
                     'myself', 'n', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither',
                     'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor',
                     'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'o', 'obviously', 'of', 'off', 'often',
                     'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others',
                     'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own', 'p',
                     'particular', 'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible',
                     'presumably', 'probably', 'provides', 'q', 'que', 'quite', 'qv', 'r', 'rather', 'rd', 're',
                     'really', 'reasonably', 'regarding', 'regardless', 'regards', 'relatively', 'respectively',
                     'right', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see',
                     'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent',
                     'serious', 'seriously', 'seven', 'several', 'shall', 'she', 'should', "shouldn't", 'since', 'six',
                     'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat',
                     'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup',
                     'sure', 't', "t's", 'take', 'taken', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx',
                     'that', "that's", 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence',
                     'there', "there's", 'thereafter', 'thereby', 'therefore', 'therein', 'theres', 'thereupon',
                     'these', 'they', "they'd", "they'll", "they're", "they've", 'think', 'third', 'this', 'thorough',
                     'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to',
                     'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying',
                     'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up',
                     'upon', 'us', 'use', 'used', 'useful', 'uses', 'using', 'usually', 'uucp', 'v', 'value', 'various',
                     'very', 'via', 'viz', 'vs', 'w', 'want', 'wants', 'was', "wasn't", 'way', 'we', "we'd", "we'll",
                     "we're", "we've", 'welcome', 'well', 'went', 'were', "weren't", 'what', "what's", 'whatever',
                     'when', 'whence', 'whenever', 'where', "where's", 'whereafter', 'whereas', 'whereby', 'wherein',
                     'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', "who's", 'whoever',
                     'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with', 'within', 'without', "won't",
                     'wonder', 'would', 'would', "wouldn't", 'x', 'y', 'yes', 'yet', 'you', "you'd", "you'll", "you're",
                     "you've", 'your', 'yours', 'yourself', 'yourselves', 'z', 'zero', '', 'attr', 'job', 'var',
                     'strong',
                     'software', 'team', 'computer', 'business', 'development', 'experience', 'td', 'suport',
                     'engineering', 'technical',
                     'resume', 'applicants', 'work'))

class Utils():
    TF_Corpus = {}
    TF_Reversed_Corpus = {}
    term_IDFs = {}
    stemmer = PorterStemmer()

    '''
            Function to remove stop words from job description and stores description as array of tokens
        '''

    def cleanAndProcess(self, soupObject):

        finalSummary = []

        if soupObject != None:
            # converting job summary tokens to lower case
            text = soupObject.getText().lower().strip()
            # using regular expressions to clean words containing unwanted characters
            text = re.sub('[^a-z\ \']+', " ", text)
            text = word_tokenize(text)
            for word in text:
                # removing stopwords from job summary
                if word not in stopWords:
                    word = self.stemmer.stem(word).encode('ascii', 'ignore')
                    finalSummary.append(word)

        return finalSummary

    '''
        Function to initiate pre-processing on data for clustering
    '''
    def process_data_for_clustering(self):
        self.buildCorpus()
        self.buildReversedCorpus()
        self.compute_TF_documents()
        self.compute_TF_IDFs()

        for job in Webscraper.jobs_fetched:
            print "ID:"+str(job.id)
            print "TF document"+str(job.TFvector)
            print "TF*IDF document"+str(job.TF_IDF)

    '''
        Function to build Corpus of terms and their frequencies in each document
    '''
    def buildCorpus(self):
        Corpus = {}

        for i in range(len(Webscraper.jobs_fetched)):
            job = Webscraper.jobs_fetched[i]
            job.set_id(i)
            for word in job.summary:
                if word not in Corpus.keys():
                    frequencies = []
                    for i in range(0, len(Webscraper.jobs_fetched)):
                        frequencies.append(0)
                    Corpus[word] = frequencies
                Corpus[word][i] += 1
        self.TF_Corpus = Corpus

    '''
        Function to reverse the corpus as job ids vs. corresponding term frequency document
    '''
    def buildReversedCorpus(self):
        ReversedCorpus = {}

        terms = self.TF_Corpus.keys()

        for i in range(0, len(Webscraper.jobs_fetched)):
            array_termFrequency = []
            for k in range(0, len(terms)):
                array_termFrequency.append(0)
            ReversedCorpus[i] = array_termFrequency

        jobIDs = ReversedCorpus.keys()

        for jobIdkey in jobIDs:
            for j in range(0, len(terms)):
                word = terms[j]
                ReversedCorpus[jobIdkey][j] = self.TF_Corpus[word][jobIdkey]

        self.TF_Reversed_Corpus = ReversedCorpus

    '''
        Function to compute term frequency vector for all fetched jobs
    '''
    def compute_TF_documents(self):

        for job in Webscraper.jobs_fetched:
            termFreq = self.TF_Reversed_Corpus[job.id]
            # finding TF for each job document
            for k in range(0, len(termFreq)):
                var1 = termFreq[k]
                var2 = sum(self.TF_Reversed_Corpus[job.id])
                job.TFvector.append(float(var1 / var2))

    '''
        Function to compute tf*idf vector for all fetched jobs
    '''
    def compute_TF_IDFs(self):

        terms = self.TF_Corpus.keys()
        jobIDs = self.TF_Reversed_Corpus.keys()

        idf_terms = {}
        for term in terms:
            termVector = self.TF_Corpus[term]
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

        self.term_IDFs = idf_terms