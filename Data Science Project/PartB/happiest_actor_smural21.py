import sys
import csv
def main():
	if (len(sys.argv) !=3):
		print ("Please enter the sentiment file followed by the csv tweet file.")
	else:
		sent_file=open("data/"+sys.argv[1])
		csv_file=csv.reader(open(sys.argv[2]))
		#To skip header row
		next(csv_file)
		#Dictionary for storing the word's sentiment score.
		sentiment_dict = {}
		for line in sent_file:
			word,score = line.split("\t")
			sentiment_dict.setdefault(word,score)
		
		#Calculating scores for the actors.
		wordScore=0
		actorScore ={}
		actorTweetCount={}
		
		for row in csv_file:
			actorScore.setdefault(row[0],0)
			actorTweetCount.setdefault(row[0],0)
			tweetScore=0
			for word in row[1].split():
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
					wordScore = int(sentiment_dict[word.lower()])
				else:
					wordScore=0
				tweetScore+=wordScore
			actorScore[row[0]]+=tweetScore
			actorTweetCount[row[0]]+=1

		sortedList=sorted(actorScore, key=actorScore.get, reverse=True)

		for actor in sortedList:
			print ((actorScore[actor]/actorTweetCount[actor]),":",(actor),end="")

if __name__ == '__main__':
    main()
