'''
Class Utils to facilitate additional functions to overall program
Author : Mayuri Wadkar
'''

from Webscraper import *
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
import math, re
from pdfdocument.document import PDFDocument
from bs4 import BeautifulSoup as Soup
import subprocess, urllib

stopWords = set(stopwords.words('english'))
stopWords.update(('a', "a's", 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after',
                     'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost', 'alone', 'along',
                     'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any',
                     'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear',
                     'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside', 'ask', 'asking',
                     'associated', 'at', 'available', 'away', 'awfully', 'b', 'be', 'became', 'because', 'become',
                     'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below',
                     'beside', 'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by',
                     "c'mon", "c's", 'came', 'can', "can't", 'cannot', 'cant', 'cause', 'causes', 'certain',
                     'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently',
                     'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could',
                     "couldn't", 'course', 'currently', 'd', 'definitely', 'described', 'despite', 'did', "didn't",
                     'different', 'do', 'does', "doesn't", 'doing', "don't", 'done', 'down', 'downwards', 'during',
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
                     'strong'))

technologies_stopwords = ['sysadmin', 'build', 'performance', 'infrastructure', 'startup', 'project-management','debugging',
                          'go','system']

actionlist_stopwords = ['personal','resume','come','veteran','motivate','assignments','manager','managers','lead','escalate',
                        'consult','engineers','participate','business','management','candidate','support','skills','senior',
                        'outsource','candidates','ensure','deliver','provide','organize','guarantee','client','referral',
                        'referrals','offer','sell','team','visa','sponsor','sponsorship','confidential','us','grow','customers',
                        'customer','lose','need','accordingly','flight','track','recommendations','goals','win','feel','hire',
                        'partnership','partnerships','emerge','emerging','supervise','employee','employees','call','team','hard',
                        'goals','goal','qualification','qualifications','qualify','qualified','qualifies','bug','defect','review',
                        'eligibility','eligible','document','documentation','teams','licence','please','talented','people','revenue',
                        'ownership','take','401k','feedback','forward','look','best','opportunity','opportunities']

class Utils():

    stemmer = PorterStemmer()

    def dotproduct(self,v1, v2):
        return sum((a * b) for a, b in zip(v1, v2))

    def length(self,v):
        return math.sqrt(self.dotproduct(v, v))

    '''
    Function to compute cosine distance between two TF-IDF vectors
    '''
    def cosine_distance(self, vector1, vector2):

        cosTheta = math.acos(self.dotproduct(vector1, vector2) / (self.length(vector1) * self.length(vector2)))
        return cosTheta

    '''
    Function to pre-process summary/ description of each job fetched
    '''
    def clean_process_summary(self, soupObject):

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
                    # word = word.encode('ascii', 'ignore')
                    word = self.stemmer.stem(word).encode('ascii', 'ignore')
                    finalSummary.append(word)

        return finalSummary

    '''
    Function to generate final pdf of course topic
    '''
    def generate_pdf(self, topic_obj):
        print 'Generating PDF..'
        path = "./PDFDocuments/"+topic_obj.topic+".pdf"

        pdf = PDFDocument(path)
        pdf.init_report()
        # pdf.h2("San Jose State University",style=pdf.style.bold)
        # pdf.h1("College of Science, Department of Computer Science",style=pdf.style.bold)
        pdf.h2("Topic Recommendation:\n")
        pdf.h1("\nTopics in "+topic_obj.topic)
        pdf.h2('\nCourse Description')
        techs = ""
        for tech in topic_obj.technologies:
            techs += tech + ", "
        pdf.p("\nIntroduction to topics in " + topic_obj.topic + " such as, "+techs)
        pdf.p(str(topic_obj.listedTech))
        pdf.h2("\nCourse Learning Outcomes:\n\n")
        pdf.p(topic_obj.actionList)
        pdf.h2("\nSummary from top job descriptions:\n")
        pdf.p(topic_obj.summary)
        pdf.generate()
        print 'PDF generated..'
        subprocess.Popen(path, shell=True)

def fetch_description_techs(url):

    technologies = set()
    joblinkTarget = Soup(urllib.urlopen(url), "html.parser")
    techTags = joblinkTarget.findAll('a', attrs={'class': 'post-tag job-link no-tag-menu'})

    for tag in range(len(techTags)):
        tech = str(techTags[tag].get_text())
        if tech not in technologies_stopwords:
            technologies.add(tech)

    job_description = joblinkTarget.find('div', attrs={'class': 'description'})
    if job_description != None:
        job_description = job_description.get_text()
    else:
        job_description = joblinkTarget.find('span', attrs={'class': 'summary'})
        if job_description != None:
            job_description = job_description.get_text()
        else:
            job_description = joblinkTarget.find('div', attrs={'itemprop': 'description'})
            if job_description != None:
                job_description = job_description.get_text()

    return job_description, technologies