###########################################################################
#Michael Siderius

#Calculating a sentiment score and location of a list of tweets using multiple functions and dictionaries to create a colored map. Need to connect the map to this main .py
#12 December 2014
###########################################################################

from math import radians, sin, cos, atan, atan2, sqrt
from simplemapplot import make_us_state_map
from time import sleep
import csv

#######################
# Name:readStateCenterFile(stateCenterDict)
# Input: StateCenterDict: Dictionary
# Output: NA
# Purpose: reads in the file of state centers as described in the handout
#######################

def readStateCenterFile(stateCenterDict):
    stateFile = open("stateCenters.txt")
    for line in stateFile:
        value = line.split(',')
        stateCenterDict[value[0]] = (float(value[1]), float(value[2]))
    stateFile.close()
    

########################
# Name:readTweetFile(tweetList)
# Input: TweetList:List
# Output:NA
# Purpose: reads the tweets from the file into a list.  The file is specified in
# the "open" command.  Change the "open" call when you want the big file. 
########################

def readTweetFile(tweetList):
    tweetFile = open("allTweets.txt", encoding="utf-8")
    for line in tweetFile: 
        try:
            value = line.split("\t")
            lat,long = value[0].split(",")
            lat = float(lat[1:])
            long = float(long[:-1])
            tweetList.append(((lat,long),str(value[3])))
        except:
            None
    tweetFile.close()

#########################    
# Name:readSentimentFile(sentimentDict)
# Input:sentimentDict:Dictionary
# Output:NA
# Purpose:this function will read in the sentiment file and create a 
# dictionary with key: word/phrase and a value: float in range -1..1
#########################

def readSentimentFile(sentimentDict):

    with open('sentimentsFull.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            sentimentDict.update({row[0]:row[1]})

###########################
# Name:distance (lat1, lon1, lat2, lon2)
# Input: (lat1, lon1, lat2, lon2)=4 floating points
# Output: Earth_radius*c; floating point of distance calculation
# Purpose:takes a latitude and longitude for two given points and returns
# the great circle distance between them in miles
###########################

def distance (lat1, lon1, lat2, lon2):

    earth_radius = 3963.2  # miles
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))
    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    dlat, dlon = lat2-lat1, lon2-lon1
    a = sin(dlat/2) ** 2  + sin(dlon/2) ** 2 * cos(lat1) * cos(lat2)
    c = 2 * atan2(sqrt(a), sqrt(1-a));
    return earth_radius * c;

###########################
# Name:color (minimum,maximum,stateSentimentScore,i)
# Input: (minimum,maximum,stateSentimentScore,i)=minimum&maximum:integers,stateSentimentScore=dict, i=integer of itereation
# Output: color:integer which represents a color of specific sentiment score.
# Purpose:calculate the color index by comparing the minimum and maximum sentiment scores.
###########################

def color(minimum,maximum,stateSentimentScore,i):

    # variables are defined to the percentages of minimum.
    minsixty = float(minimum * .6)
    minthirty = float(minimum * .3)
    minfifteen = float(minimum * .15)

    # variables are defined to the percentages of maximum.
    maxsixty = float(maximum * .6)
    maxthirty = float(maximum * .3)
    maxfifteen = float(maximum * .15)

    keys=stateSentimentScore.keys()
    values=stateSentimentScore.values()

    #finding the color by comparing min and maximum sentiment scores.
    #Using inequalities to sort the values
    #First sort if 0,negative or positive
    #Then find color according to designated range.
    
    if i==0:
        color=4       

    elif float(i)<float(0):
        if minfifteen<i<0 :
            color=3
  
        elif minthirty<i<minfifteen:
            color=2

        elif minsixty<i<minthirty:
            color=1

        elif i<minsixty:
            color=0
      
    elif float(i)>float(0):
        if 0<i<maxfifteen:
            color=5

        elif maxfifteen<i<maxthirty:
            color=6
  
        elif maxthirty<i<maxsixty:
            color=7

        elif i>maxsixty:
            color=8

    return color


###########################
# Name:getWordOfInterest()
# Input: NA
# Output: WordOfInterest:string
# Purpose: asks for user input, lowercases input and returns the wordOfInterest
###########################

def getWordOfInterest():

    #user input, setting the input to lower case
    wordOfInterest = input("what word are you looking for? ")
    wordOfInterest = wordOfInterest.lower()

    return wordOfInterest


###########################
# Name:findInterestList()
# Input: tweetList:List, wordOfInterest:string
# Output: InterestList:List, InterestState:List
# Purpose: To create  list. InterestList is list of tweets with the word of interest.
###########################

def findInterestList(tweetList,wordOfInterest):

    #Initilizing an empty list
    #InterestList=Tweets that contain user inputted word of interest
    #InterestSTate=State where the tweet that contains word of interest

    InterestList=[]

    
    #iterating through the tweetList.
    #if wordOfInterest exists in the lowercased index position 1, add to InterestList

    for i in tweetList:
        if wordOfInterest in i[1].lower():
            InterestList.append(i)

    return InterestList


###########################
# Name:findInterestState()
# Input: InterestList:List, stateCenterDict:Dictionary
# Output: InterestState:List
# Purpose: To create  list. InterestSTate is list of states where tweets that contain word of interest exist.
###########################

def findInterestState(InterestList,stateCenterDict):

    #Initilizing list
    InterestState=[]

    #iterating through IntersetList
    #point=latitude 
    
    for i in InterestList:
        point=i[0]

        #arbitrary number that needed to be bigger than the Longitude to determine the closest state.
        #initilizing minState with empty data
        tempMinimum=400
        minState=None


        #exceptions of states:Alaska, hawaii are determined by lattitude position.
        #if: set minState to state abbreviation
        if point[0]>55:
            minState="AK"

        elif point[0]<26:
            minState="HI"

        #Rest of the states
        #calculates the nearest state of the tweet by using distance function
        
        else:

            for state in stateCenterDict:
                center = stateCenterDict[state]

                distanceCalculation=distance(point[0],point[1],center[0],center[1])

                #redefines tempMinimum to calculate nearest state,assign minState to state
                if distanceCalculation<tempMinimum:
                    tempMinimum=distanceCalculation
                    minState=state

        #append minState to InterestState List
        InterestState.append(minState)

    return InterestState

###########################
# Name:updateScores(InterestList,sentimentDict,InterestState,stateSentimentScore)
# Input: InterestList:LIst,sentimentDict:Dictionary,InterestState:List,stateSentimentScore:Dict
# Output: SentimentScore:float stateSentimentScore:Dict
# Purpose: count the sentiment scores according to the existing state.
###########################

def updateScores (InterestList,sentimentDict,InterestState,stateSentimentScore):

    #Initilizing tweetNumber to keep track of list position
    tweetNumber=0

    #iterate through the InterestList
    for i in InterestList:

        #Initializing tweet to InterestList's at index position 1, which is the list of Tweets.
        #Intialing sentimentScore to 0. sentimentScore is the running total. 
        tweet = i[1]
        sentimentScore=0
        
        # If the lowercased phrase is in lowercase tweet of the SentimentDict, add that score to SentimentScore
        for phrase in sentimentDict:
            if phrase.lower() in tweet.lower():
                sentimentScore=sentimentScore+float(sentimentDict[phrase])

        indexInterestState=InterestState[tweetNumber]


        #If the index position does not have data, then add SentimentScore to that position. 
        if indexInterestState != None:
            stateSentimentScore[indexInterestState] += sentimentScore
        
        tweetNumber=tweetNumber+1


    return sentimentScore, stateSentimentScore

###########################
# Name:findMinimum(values)
# Input: values:values from stateSentimentScore dict. 
# Output: minimum=float
# Purpose: calculates the minimum sentiment value in the stateSentimentScore
###########################

def findMinimum(values):

    #A very LARGE arbitary number to count down from. This determines the minimum
    score=800

    for i in values:
        if float(i) < score:
            score=float(i)
    minimum=float(score)

    return minimum

    
###########################
# Name:findMaximum(values)
# Input: values:values from stateSentimentScore dict. 
# Output: maximum=float
# Purpose: calculates the maximum sentiment value in the stateSentimentScore
###########################

def findMaximum(values):

    #A very SMALL arbitary number to count up from. This determines the maximum. 
    score=0
    
    for i in values:
        if float(i)>score:
            score=float(i)
    maximum=float(score)

    return maximum


###########################
# Name: colorDictionary()
# Input: minimum: float; maximum: float; stateSentimentScore: Dict
# Output: stateSentimentScore: Dict
# Purpose: Updates the color to the StateSentimentScore's Dictionary. 
###########################

def colorDictionary(minimum,maximum,stateSentimentScore):

    # On each iteration, changing the index position to color. 
    for j in stateSentimentScore:
        i=stateSentimentScore[j]
        findColor=color(minimum,maximum,stateSentimentScore,i)
        stateSentimentScore[j]=findColor

    return(stateSentimentScore)


############################

############################
#MAIN
############################
def main():

    #initilizing dictionaries and lists
    stateCenterDict = {}                #Key: state abbrev  Value: 2-tuple of (lat,long) of state center
    tweetList = []                      #list of two items, first is 2-tuple (lat,long), second is tweet
    sentimentDict = {}                  #Key: words/phrases Value: sentiment score from -1 .. 1 for each word

    #Initilizing these two dictionaries
    stateSentimentScore = {}     
    stateCountDict = {}


    #opening the sentimentDictionary using the readSentimentFile function
    readSentimentFile(sentimentDict)

    #reading the stateCenterDict file with the function readStateCenterFile
    readStateCenterFile(stateCenterDict)

    #reading and opening the tweetList file using the readTweetFile function
    readTweetFile(tweetList)

    #Setting the values of the stateCountDict and stateSentimentScore to 0 at each index for future use
    for state in stateCenterDict.keys():
        stateCountDict[state] = 0
        stateSentimentScore[state] = 0

    #Getting user input
    wordOfInterest=getWordOfInterest()

    #creating the InterestList of tweets that have the word of Interest in it.
    #Using the findInterestList function
    InterestList=findInterestList(tweetList,wordOfInterest)

    #creating the interestState list, from findInterestState function. which is states that the tweets of interest are in.
    InterestState=findInterestState(InterestList,stateCenterDict)

    #if there is no data in index i, add 'addToDict' to the dictionary at that index position.
    for i in InterestState:
        if i != None:
            g=InterestState.count(i)
            addToDict={i:g}
            stateCountDict.update(addToDict)
        
    #updating the sentimentScore, and the statSentimentScore by calling the updateScores function
    sentimentScore, stateSentimentScore=updateScores(InterestList,sentimentDict,InterestState,stateSentimentScore)

    #sorts the stateCountDict keys by alphabetical order. for each state,divides the score by how many tweets in that state, creating the average
    #print out the data
    for state in sorted(stateCountDict.keys()):
        if stateCountDict[state] != 0:
            stateSentimentScore[state] = stateSentimentScore[state]/stateCountDict[state]
            print(state, stateCountDict[state], stateSentimentScore[state])
        else:
            print(state, stateCountDict[state], stateSentimentScore[state])
            

    #calling the findMaximum and findMinimum functions to determine the min and max scores of the list. 
    values=stateSentimentScore.values()
    minimum=findMinimum(values)
    maximum=findMaximum(values)

    #This calls the colorDictionary to create the final stateSentimentScore to be used in the coloring of the US map
    stateSentimentScore=colorDictionary(minimum,maximum,stateSentimentScore)


    ##################
    #I used color brewer to help me pick the colors.
    #Red represents positive sentiment, shading to orange and yellow for less positive senitment.
    #Light gray means no data.
    #Dark blue represents negative sentiment, shading to light blue for less negative sentiment.
    ####INDEX#########[     0          1         2          3          4          5          6          7           8   ]  
    SENTIMENTCOLORS = ["#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#bababa", "#fee090", "#fdae61", "#f46d43", "#d73027"]
    ####COLOR#########["darkblue", "blue", "lightblue", "lightcyan", "lightgray", "yellow", "orange", "darkorange", "red"] 

    make_us_state_map(stateSentimentScore, SENTIMENTCOLORS)


#############################   
main()
    

