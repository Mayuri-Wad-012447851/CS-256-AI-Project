from rake_nltk import Rake
from gensim.summarization import summarize
from nltk import word_tokenize, pos_tag, ne_chunk
import nltk, urllib
from nltk.stem.wordnet import WordNetLemmatizer
from Utils import stopWords
from bs4 import BeautifulSoup as Soup
from Utils import actionlist_stopwords

class SummarizationModule:

    def summarize_job_descriptions(self, text):

        return summarize(text)

    def get_topic(self, text):
        topicRake = Rake()
        topicRake.extract_keywords_from_text(text)
        topicExtractor = topicRake.get_ranked_phrases()

        topic = ""
        for temp_topic in topicExtractor:
            junk = False
            if len(temp_topic) <= 50:
                for word in temp_topic:
                    if word in stopWords:
                        junk = True
                        break
                if junk == False:
                    topic = temp_topic

                    if topic.endswith("ineer"):
                        topic += "ing"
                    elif topic.endswith("oper"):
                        topic = topic[:-2] + "ment"
                    break

        return topic

    def get_listed_tech_and_action_list(self, text):

        lemmatizer = WordNetLemmatizer()
        r = Rake()

        listedTech = ""
        r.extract_keywords_from_text(text)

        rankedPhrases = r.get_ranked_phrases()  # To get keyword phrases ranked highest to lowest.
        for eachPhrase in rankedPhrases:
            toChange = eachPhrase
            eachPhrase = str(eachPhrase.encode('ascii', 'ignore'))
            rankedPhrases[rankedPhrases.index(toChange)] = eachPhrase

        actionList = ""
        for sent in rankedPhrases:
            flag_junk = False
            content = ne_chunk(pos_tag(word_tokenize(sent)))
            if len(content) > 1 and content[0][1][0] == 'V':
                sentList = sent.split()
                sentList[0] = lemmatizer.lemmatize(content[0][0], 'v')
                rankedPhrases.remove(sent)
                sent = ""
                for i in sentList:
                    sent = sent + " " + i
                for word in sent:
                    if (word in actionlist_stopwords):
                        flag_junk = True
                        break
                if flag_junk == False:
                    actionList = actionList + sent + "\n"

        if len(rankedPhrases) > 6:
            for each in range(0, 4):
                listedTech = listedTech + rankedPhrases[each] + ", "
            listedTech += rankedPhrases[4]

        return listedTech, actionList