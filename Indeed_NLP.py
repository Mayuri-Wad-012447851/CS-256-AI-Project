'''
Module to extract technologies, action lists and summary from job description
Author : Samanvitha Basole
'''

# -*- coding: utf-8 -*-
import collections

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


from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib



# https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def makeDescription(title, text):
    lemmatizer = WordNetLemmatizer()
    r = Rake()

    topicRake = Rake()
    topicRake.extract_keywords_from_text(title)
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

print ("\nClass 1 ---------------------------------------------------------------------------------------")
html = urllib.urlopen('https://www.indeed.com/viewjob?jk=296caa11735a0601&q=computer+science&l=Fremont%2C+CA&tk=1c0n8p16bbi56cng&from=web').read()
text = text_from_html(html)
makeDescription("Principal Software Engineer - Full Stack", text)

print ("\nClass 2 ---------------------------------------------------------------------------------------")
html = urllib.urlopen('http://search.lockheedmartinjobs.com/ShowJob/Id/92631/Software%20Engineer')
text = text_from_html(html)
makeDescription("Software Engineer", text)


print ("\nClass 3 ---------------------------------------------------------------------------------------")
html = urllib.urlopen('https://workday.wd5.myworkdayjobs.com/en-US/Workday/job/USA-CA-Pleasanton/Software-Application-Engineer--All-Levels---Enterprise-Cloud-Applications---HCM_JR-22238?utm_source=indeed.com&utm_campaign=SEM&utm_medium=paid_search&utm_content=job_aggregator&ss=paid&source=website_indeed')
text = text_from_html(html)
makeDescription("Software Application Engineer (All Levels), Enterprise Cloud Applications – HCM", text)


print ("\nClass 4 ---------------------------------------------------------------------------------------")
html = urllib.urlopen('https://www.indeed.com/viewjob?jk=fd4b905176510e48&q=computer+science&l=Fremont%2C+CA&tk=1c0n8p16bbi56cng&from=web')
text = text_from_html(html)
makeDescription("Field Test Engineer - Autonomous Vehicles", text)
