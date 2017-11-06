from Job import *
from bs4 import BeautifulSoup as Soup
import re,urllib

class IndeedScraper(object):

    jobsFetched = []

    '''
        Function to scrape Computer Science jobs from indeed.com
    '''
    def start(self):
        print '\nFetching jobs from indeed.com'

        urlKeyword = "Computer Science"
        webURL = "http://www.indeed.com/jobs?q=" + urlKeyword + "&start="

        for page in range(1, 101):
            page = (page - 1) * 10
            url = "%s%d" % (webURL, page)
            target = Soup(urllib.urlopen(url), "html.parser")

            targetElements = target.findAll('div', attrs={'class': ' row result'})
            if targetElements == []:
                break
            for element in targetElements:
                try:
                    # creating a job instance to store details like job title, company, address, JobLink
                    job = Job()

                    company = element.find('span', attrs={'class': 'company'})
                    if company != None:
                        job.companyName = company.getText().strip()
                    title = element.find('a', attrs={'class': 'turnstileLink'}).attrs['title']

                    if title != None:
                        job.jobTitle = title.strip()

                    addr = element.find('span', attrs={'class': 'location'})
                    if addr != None:
                        job.address = addr.getText().strip()

                    job.homeURL = "http://www.indeed.com"
                    job.jobLink = "%s%s" % (job.homeURL, element.find('a').get('href'))

                    skillsElement = element.find('span', attrs={'class': 'experienceList'})
                    job.skills = self.cleanAndProcess(skillsElement)

                    summaryElement = element.find('span', attrs={'class': 'summary'})
                    job.summary = self.cleanAndProcess(summaryElement)

                    if ((job.jobLink != "") and (job.jobLink != None)):
                        joburl = urllib.quote(job.jobLink.encode('utf8'), ':/')
                        joblinkTarget = Soup(urllib.urlopen(joburl), "html.parser")
                        summaryElement = joblinkTarget.find('span', attrs={'class': 'summary'})
                        job.summary.extend(self.cleanAndProcess(summaryElement))

                    if (job.jobTitle != None and job.jobLink != None):
                        self.jobsFetched.append(job)
                        print job.jobTitle

                except Exception as e:
                    print e.message
                    continue

        print 'Fetching jobs from indeed.com completed.'
        return self.jobsFetched

    '''
        Function to remove stop words from job description and stores description as array of tokens
    '''
    def cleanAndProcess(self,soupObject):
        stopwords = ['a', "a's", 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after',
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
                     "you've", 'your', 'yours', 'yourself', 'yourselves', 'z', 'zero', '', 'attr', 'job','var','strong']
        finalSummary = []

        if soupObject != None:
            #converting job summary tokens to lower case
            text = soupObject.getText().lower().strip()
            #using regular expressions to clean words containing unwanted characters
            text = re.sub('[^a-z\ \']+'," ", text)
            text = text.split(" ")
            for word in text:
                #removing stopwords from job summary
                if word not in stopwords:
                    word = word.encode('ascii', 'ignore')
                    finalSummary.append(word)

        return finalSummary