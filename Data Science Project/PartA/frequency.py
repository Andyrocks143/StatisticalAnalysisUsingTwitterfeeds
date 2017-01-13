import sys
import json

def main():
    #1st arguement is the stopwords file.
    stop_word_file = open("data/stopwords.txt")
    #Stopwords for storing the stop words in a list.
    stopword = []
    tweets=[]
    wordList = {}
    #2nd word is the tweet file to parse.
    tweet_file = open("breaking_bad_tweets_smural21.csv,'r')
    #TODO: Implement
    
    #Creating the stop words list.
    for line in stop_word_file:
    	stopword.append(line[:-1])
    stopwords=set(stopword)
    for line in tweet_file:
    	jsresult = (json.loads(line))
    	tweets.append(jsresult['text'])
    
    validWordcount = 0
    totalWordCount=0
    for tweet in tweets:
        for word in tweet.split():
            totalWordCount+=1
            #Checking for the stopwords from the set of stopwords provided to us.
            if word.lower() not in stopwords:
                validWordcount+=1
                #If word already present and is encountered again, increase the term occurance by 1.
                if word.lower() in wordList:
                    wordList[word.lower()]+=1
                else:    
                #If word is not yet encountered, create a new key in the dictionary and set value as 1.
                    wordList.setdefault(word.lower(),1)
    
    termFrequency = {}
    #Generating the term frequency values for the words.
    for key in wordList.keys():
        termFrequency.setdefault(key,(wordList[key]/validWordcount))
    
    #Sorting based on the term frequency values
    sortedtermFrequency = sorted(termFrequency, key=termFrequency.get, reverse=True)
    #Printing all words and their term frequencies.
    for values in sortedtermFrequency:
        print (values,termFrequency[values])
    
    
if __name__ == '__main__':
    main()
