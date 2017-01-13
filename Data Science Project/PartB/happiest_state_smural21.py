import sys
import json
import csv

def main():
    sent_file = open("data/"+sys.argv[1])
    tweet_file = open(sys.argv[2])

    #Dictionary for the word's sentiment scores.
    sentiment_dict={}
    for line in sent_file:
            word,score = line.split("\t")
            sentiment_dict.setdefault(word,score)

    #Dictionaries for storing state sentiment scores and tweet counts.
    stateSentiment={}
    stateTweetCount={}

    #1. Placing the states and their abbreviations in a dictionary. 2. Creating a dictionary for the state, sentiment score and tweet count.
    states={}
    states_file = open("data/USAstates.csv",'r')
    statesReader = csv.reader(states_file)
    for row in statesReader:
        states.setdefault(row[0],row[1])
        stateSentiment.setdefault(row[0],0)
        stateTweetCount.setdefault(row[0],0)
    
    
    #Reading every tweet and assigning a score first.
    for line in tweet_file:
        places=[]
        userLocation=[]
        coordinates=[]
        stateList=[]
        jsresult = (json.loads(line))
        tweet_score = 0
        tweet = jsresult['text']
        for word in (tweet.split()):
            if (word.lower().isalpha()==False):
                    word=word.replace("!","")
                    word=word.replace("@","")
                    word=word.replace(".","")
                    word=word.replace('"',"")
                    word=word.replace(',',"")
                    word=word.replace('?',"")
                    word=word.replace('#',"")
                    word=word.replace(':',"")
                    word=word.replace(')',"")
                    word=word.replace('(',"")
                    word=word.replace("'","")
            if (word.lower() in sentiment_dict.keys()):
                word_score = int(sentiment_dict[word.lower()])
            else:
                word_score = 0
            tweet_score+=word_score
        
        #Now that the tweet score has been calculated, find states related to the tweet and assign the score to that state.
        if (jsresult['place']!= None):
            places.append(jsresult['place'])
        if (jsresult['user']['location']!= None):
            userLocation.append(jsresult['user']['location'])        
        if(jsresult['coordinates']!=None):
            coordinates.append(jsresult['coordinates'])
        relatedStates=[]
        #Checking in the userLocation attribute for any location information. If any state is found, add them to a 'relatedstates' list.
        for place in userLocation:
            #First checking for words of the format <city, State> eg: <miami, FLorida> or <miami,FL>.
            if ("," in place):
                place=place.replace(", ",",")
                test = place.split(",")
                if (test[1].upper() in states.keys()):
                    relatedStates.append(test[1].upper())
                    ###(test[1].upper(),"--",place)
                elif (test[1].upper() in (name.upper() for name in states.values())):
                    for k,v in states.items():
                        if (test[1].upper() == v.upper()):
                            state=k
                            relatedStates.append(state)
                            ###(state,'--',place)
                #Check for places in the string of the format <State, USA>.eg: <Florida, USA> or <FL, USA>.
                elif (test[1].upper() == "USA"):
                    if (test[0].upper() in (name.upper() for name in states.values())):
                        for k,v in states.items():
                            if (test[0].upper() == v.upper()):
                                state=k
                                relatedStates.append(state)
                                ###(state,'--',place)
                #Finally, check the remaining words by splitting each word.
                else:
                    for t in test:
                        if (t.rstrip(" ").rstrip('.').lower() in (name.lower() for name in states.values())):
                            for k,v in states.items():
                                if (t.rstrip(" ").rstrip('.').lower() == v.lower()):
                                    state=k
                                    relatedStates.append(state)
                                    ###(state,'--',place)
                        if (t.rstrip(" ").rstrip('.').lower() in (name.lower() for name in states.keys())):
                            for k,v in states.items():
                                if (t.rstrip(" ").rstrip('.').lower() == k.lower()):
                                    state=k
                                    relatedStates.append(state)
                                    ###(state,'--',place)
            #Check for any mention of a state name in the location string. Eg: Guy from TX.            
            else:
                #Avoid common words which intersect with state abbreviations.
                commonWords=["me","Me","in","In","ok","Ok","de","or"]
                words=place.split()
                for word in words:
                    #First Check if word is a state abbreviation.
                    if (word.rstrip(" ").rstrip(".").lower() in (name.lower() for name in states.keys())):
                        if (word not in commonWords):
                            state1 = word.rstrip(" ").rstrip(".").upper()
                            relatedStates.append(state1)
                            ###(state1,'---',place)
                    #Then check if it is the full state name. 
                    elif (word.rstrip(" ").rstrip(".").lower() in (name.lower() for name in states.values())):
                        for k,v in states.items():
                            if (word.rstrip(" ").rstrip(".").lower() == v.lower()):
                                state=k
                                relatedStates.append(state)
                                ###(state,"---",place)
        #Checking in places attribute.                    
        for w in places:
            if (w['country'].lower() == "united states"):
                if (len(w['full_name']) != 0):
                    places = w['full_name'].split(",")
                    if (len(places)!=1):
                        #For data of the format <city, State abbreviation> eg: <Miami, FL>
                        if (places[1].rstrip(" ").replace(" ","").upper() in states.keys()):
                            relatedStates.append(places[1].rstrip(" ").replace(" ","").upper())
                            
                        #For data of the format <State, USA> Eg:<Utah, USA> or <IL, USA>
                        elif (places[1].replace(" ","").upper() == "USA"):
                            if(places[0].rstrip(" ") in states.keys()):
                                relatedStates.append(places[0].rstrip(" ").upper())
                                
                            elif (places[0].rstrip(" ").lower() in (name.lower() for name in states.values())):
                                for k,v in states.items():
                                    if (places[0].rstrip(" ").rstrip(".").lower() == v.lower()):
                                        state=k
                                        relatedStates.append(state)
                                        
        #Finally, for every state related to the tweet, increase the tweet count and add up the tweet sentiment score.
        for state in relatedStates:
            stateTweetCount[state]+=1
            stateSentiment[state]+=tweet_score
    
    stateScore={}
    #For each state, compute the average sentiment score.
    for state in stateSentiment:
        if (stateTweetCount[state]!=0):
            Score=(stateSentiment[state]/stateTweetCount[state])
        else:
            Score=0
        stateScore.setdefault(state,Score)

    #Sort the list accoording to the score.
    finalScore =sorted(stateScore,key=stateScore.get,reverse=True)

    #Print the final output with average sentiment score upto 4 decimal places for efficient comparison.
    for state in finalScore:
        print(("{0:.4f}".format(stateScore[state])),": ",state)
    
    
if __name__ == '__main__':
    main()
