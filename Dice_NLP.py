'''
Module to extract technologies, action lists and summary from job description
Author : Samanvitha Basole
'''
# -*- coding: utf-8 -*-
import collections

from rake_nltk import Rake
from gensim.summarization import summarize
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
    summaryElement = joblinkTarget.find('div', attrs={'id': 'jobdescSec'})
    text = summaryElement.get_text()

    topicFromHTML = joblinkTarget.find('h1', attrs={'class': 'jobTitle'}).text

    topicRake = Rake()
    topicRake.extract_keywords_from_text(topicFromHTML)
    topicExtractor = topicRake.get_ranked_phrases()
    topic = topicExtractor[0]
    if topic.endswith("ineer"):
        topic += "ing"
    elif topic.endswith("oper"):
        topic = topic[:-2] + "ment"
    elif topic.endswith("yst"):
        topic = topic[:-1] + "is"


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
    print ("Introduction to topics in " + topic + " such as " + listedTech)

    print ("\nCourse Learning Outcomes: -----------------------------------------------------------------")
    print actionList
    keywordsText = []
    print ('Summary:')

    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(text)

    text = ""

    for each in sentences:
        text = text + " " + str(each.encode('ascii','ignore'))

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
makeDescription("https://www.dice.com/jobs/detail/Software-Engineer-The-Armada-Group-Sunnyvale-CA-94089/armada/8104?icid=sr7-1p&q=computer+science&l=San%20Jose,%20CA")

print ("Class 2:   *************************************************************")
makeDescription("https://www.dice.com/jobs/detail/Computer-Scientist-%26%2345-Algorithm-%26%2345-Algorithm-Development%2C-C%2B%2B%2C-Com-CyberCoders-Livermore-CA-94550/cybercod/SG1%26%234514183182?icid=sr3-1p&q=computer+science&l=San%20Jose,%20CA")
print ("Class 3:   *************************************************************")
makeDescription("https://www.dice.com/jobs/detail/Data-Analyst-Advantage-Sunnyvale-CA-94086/tacman/Advantage_3076%26%2345747?icid=sr11-1p&q=computer+science&l=San%20Jose,%20CA")
