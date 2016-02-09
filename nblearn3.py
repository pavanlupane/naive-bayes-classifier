#!/usr/bin/python3
import os
import sys
import string
import json
import collections
from collections import Counter

conditionalProb = {'positive':{},'negative':{},'truthful':{},'deceptive':{}}

def findCondProb(docClassA,docClassB,token):
        totalWordCount = len(docClassA)
        vocabList = set(docClassA + docClassB)
        vocabListLen = len(vocabList)
        ctr = Counter(docClassA)
        
        for wordToken in vocabList:
            if wordToken not in conditionalProb[token].keys():
                probValue = 0
                wordCount = ctr[wordToken]
                
                
                probValue = (wordCount + 1.0) / (totalWordCount + vocabListLen)
                conditionalProb[token][wordToken] = probValue
            else:
                continue
def isNumber(digitString):
    return digitString.isdigit()
                 
def processWord(word):
    procWord = "".join(l for l in word if l not in string.punctuation)
    stopWords = ["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours    ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]
    procWord = procWord.lower()
    if procWord in stopWords:
        return 'stop'
    elif(isNumber(procWord)):
        return 'stop'
    return procWord
              
def main():
    positiveClass = list()
    negativeClass = list()
    truthfulClass = list()
    deceptiveClass = list()
    
       
    for root, dirs, files in os.walk(sys.argv[1],topdown=True):  
        for name in files:
            path = os.path.join(root, name)
            if"positive" in path and ".txt" in path:
                if "truthful" in path:      #add to truthful dataset
                    with open(path,'r') as f:
                        for line in f:
                            for word in line.split():
                                myWord = processWord(word)
                                if myWord != 'stop':
                                    positiveClass.append(myWord)
                                    truthfulClass.append(myWord)
                 
                if "deceptive" in path:     #add to deceptive dataset
                    with open(path,'r') as f:
                        for line in f:
                            for word in line.split():
                                myWord = processWord(word)
                                if myWord != 'stop':
                                    positiveClass.append(myWord)
                                    deceptiveClass.append(myWord)

            if "negative" in path and ".txt" in path:
                if "truthful" in path:      #add to truthful dataset
                    with open(path,'r',) as f:
                        for line in f:
                            for word in line.split():
                                myWord = processWord(word)
                                if myWord != 'stop':
                                    negativeClass.append(myWord)
                                    truthfulClass.append(myWord)
                    
                if "deceptive" in path:     #add to deceptive dataset
                    with open(path,'r') as f:
                        for line in f:
                            for word in line.split(' '):
                                myWord = processWord(word)
                                if myWord != 'stop':
                                    negativeClass.append(myWord)
                                    deceptiveClass.append(myWord)
    
    findCondProb(positiveClass,negativeClass,"positive")
    findCondProb(negativeClass,positiveClass,"negative")
    findCondProb(deceptiveClass,truthfulClass,"deceptive")
    findCondProb(truthfulClass,deceptiveClass,"truthful")
        
    with open('nbmodel.txt','w') as fout:
        json.dump(conditionalProb,fout)
        

if __name__ == "__main__":main()