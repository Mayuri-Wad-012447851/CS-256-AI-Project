# -*- coding: utf-8 -*-
import collections

#######   works only for stack overflow links   ###########

from rake_nltk import Rake
from gensim.summarization import summarize
from gensim.summarization import keywords
from bs4 import BeautifulSoup
import urllib
from nltk import word_tokenize, pos_tag, ne_chunk
import nltk
import os
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')

def makeDescription(url):
    lemmatizer = WordNetLemmatizer()
    r = Rake()
    joblinkTarget = BeautifulSoup(urllib.urlopen(url), "html.parser")
    summaryElement = joblinkTarget.find('div', attrs={'class': 'description'})
    text = summaryElement.get_text()

    techTags = joblinkTarget.findAll('a', attrs={'class': 'post-tag job-link no-tag-menu'})

    topicFromHTML = joblinkTarget.find('a', attrs={'class': 'title job-link'}).text
    topicRake = Rake()
    topicRake.extract_keywords_from_text(topicFromHTML)
    topicExtractor = topicRake.get_ranked_phrases()
    topic = topicExtractor[0]
    if topic.endswith("ineer"):
        topic += "ing"
    elif topic.endswith("oper"):
        topic = topic[:-2] + "ment"

    techSet = set()

    if len(techTags) >= 3:
        for tag in range(0, 3):
            techSet.add(str(techTags[tag].get_text()))
        techSet = list(techSet)
        technologies = techSet[0] + ", " + techSet[1] + ", " + techSet[2] + ", "
    else:
        technologies = ""

    listedTech = ""
    r.extract_keywords_from_text(text)

    rankedPhrases = r.get_ranked_phrases() # To get keyword phrases ranked highest to lowest.
    for eachPhrase in rankedPhrases:
        toChange = eachPhrase
        eachPhrase = str(eachPhrase.encode('ascii', 'ignore'))
        rankedPhrases[rankedPhrases.index(toChange)] = eachPhrase

    actionList = ""
    for sent in rankedPhrases:
        content = ne_chunk(pos_tag(word_tokenize(sent)))
        if len(content) > 1 and content[0][1][0] == 'V':
            sentList = sent.split()
            sentList[0] = lemmatizer.lemmatize(content[0][0], 'v')
            rankedPhrases.remove(sent)
            sent = ""
            for i in sentList:
                sent = sent + " " + i
            actionList = actionList + sent + "\n"

    if len(rankedPhrases) > 6:
        for each in range(0, 4):
            listedTech = listedTech + rankedPhrases[each] + ", "
        listedTech += rankedPhrases[4]

    print ("\nTopic: -----------------------------------------------------------------------------------")
    print ("Topics in " + topic + "\n")
    print ("Course Description: ----------------------------------------------------------------------")
    print ("Introduction to topics in " + topic + " such as " + technologies + listedTech)

    print ("\nCourse Learning Outcomes: -----------------------------------------------------------------")
    print actionList
    keywordsText = []
    print ('Summary:')
    print (summarize(text))
    print ("\n")

    '''
    print ('Keywords:')
    temp = ""
    for keyword in keywords(text):
        if keyword.decode('utf-8').encode('ascii','ignore') == '\n':
            keywordsText.append(temp.decode('utf-8').encode('ascii','ignore'))
            temp = ""
        else:
            temp += keyword

    print keywordsText

    counter = collections.Counter(keywordsText)
    print(counter.most_common())
    '''

    # print all phrases starting with verb
    # add them to a actionsList
    # print them in CLOs

print ("Class 1:   *************************************************************")
makeDescription("https://stackoverflow.com/jobs/162149/full-stack-software-engineer-visor?so=i&pg=1&offset=0")
print ("Class 2:   *************************************************************")
makeDescription("https://stackoverflow.com/jobs/158439/senior-software-engineer-at-google-google?so=i&pg=1&offset=1")
print ("Class 3:   *************************************************************")
makeDescription("https://stackoverflow.com/jobs/154343/senior-full-stack-engineer-synthego?so=i&pg=1&offset=2")
print ("Class 4:   *************************************************************")
makeDescription("https://stackoverflow.com/jobs/159265/backend-engineer-perceptai?so=i&pg=1&offset=10")

