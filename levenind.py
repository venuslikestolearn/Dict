from itertools import *
from collections import Counter
import os,sys
def nearestBoolVectors(boolVector,l):
	words=[]
	tolerance=2
	possibleVectors=[]
	for i in range(-1*tolerance,tolerance):
		try:
			possibleVectors.extend(lenDict[i+l])
		except RuntimeError:
			pass
	for vector in possibleVectors:
		count=0
		for ai,bi in zip(vector,boolVector):
			if ai!=bi:
				count+=1
		if count<=int(sys.argv[6]):
			words.extend(MemDict[vector])
	return words

def DictSearch(testlist):
	boolVector=getBoolVector(testlist)
	l=len(testlist)
	if boolVector in MemDict:
		words = MemDict[boolVector]
		return findCandidates(testlist,words)
		#print("Finding candidates")
		#return timeof(findCandidates,testlist,words)
	else:
		words = nearestBoolVectors(boolVector,l)
		#print("Finding closest boolean vectors")
		#words = timeof(nearestBoolVectors,boolVector,l)
		return findCandidates(testlist,words)
		#print("Finding candidates")
		#return timeof(findCandidates,testlist,words)

def findCandidates(testlist,wordList):
	Candidates=[]
	for wordDict in wordList:
		dWord =''.join(wordDict)
		if wordDict==testlist:
			Candidates=[]
			Candidates.append(dWord)
			return(Candidates)
		else:
			testLen = len(testlist)
			dictLen = len(wordDict)
			if testLen==1 and dictLen<=2:
				#add all  dictionary words with length 1,2
				Candidates.append(dWord)
			elif testLen==2 and (testLen+1 >= dictLen >= testLen-1):
				Candidates.append(dWord)
			elif 3<=testLen<=6 and (testLen+2 >= dictLen >= testLen-2):
				Candidates.append(dWord)
			elif (testLen+4 >= dictLen >= testLen-4) :
				Candidates.append(dWord)
	return(Candidates)

# http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
def levenshtein(s, t):
    m, n = len(s), len(t)
    d = [range(n+1)]
    d += [[i] for i in range(1,m+1)]
    for i in range(0,m):
        for j in range(0,n):
            cost = 1
            if s[i] == t[j]: cost = 0

            d[i+1].append( min(d[i][j+1]+1, # deletion
                               d[i+1][j]+1, #insertion
                               d[i][j]+cost) #substitution
                           )
    return d[m][n]


def dict_words(dictfile="/home/venus/Desktop/Dict"):
    "Return an iterator that produces words in the given dictionary."
    return filter(len,
                   map(str.strip,
                        open(dictfile)))


def timeof(fn, *args):
    import time
    t = time.time()
    res = fn(*args)
    print ("time: ", (time.time() - t))
    return res

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def getBoolVector(wordDict):
	boolVector=[]
	for char in alphabets:
		if char in wordDict:
			boolVector.append(True)
		else:
			boolVector.append(False)
	return tuple(boolVector)

def createDictionary(MemDict,Dictionary,lenDict):
	with open(Dictionary,'r') as inDict:
		for line in inDict:
			wordDict=line.strip().split()
			l=len(wordDict)
			#print("getBoolVector")
			#boolVector=timeof(getBoolVector,wordDict)
			boolVector=getBoolVector(wordDict)
			if l in lenDict:
				lenDict[l].append(boolVector)
			else:
				lenDict[l]=[boolVector]
			if boolVector in MemDict:
				MemDict[boolVector].append(wordDict)
			else:
				MemDict[boolVector]=[wordDict]

def findLeven(Candit,words,obj):
	d=int(float(len(words.strip()))*0.5)+1
	#print(d)
	for item in Candit:
		dd=levenshtein(''.join(item),words.strip())
		if dd<d:
			d=dd
			obj=item
	return (d, obj)

if __name__ == "__main__":
	mainDir = sys.argv[1]
	outputDir = sys.argv[2]
	Dictionary=sys.argv[3]
	vocabFile = sys.argv[4]
    #Dictionary - keys:boolean vector, values: list of words (each word as list of chars)
	MemDict = {}
	#Dictionary - keys:word length, values: list of boolean vector (each word as list of chars)
	lenDict = {}
    #Reference list used to create the boolean vectors
	alphabets = []
	with open(vocabFile,'r') as vocab:
		for line in vocab:
			alphabets.append(line.strip())
	createDictionary(MemDict,Dictionary,lenDict)
	#print("Dictionary creation time in s")
	#timeof(createDictionary,MemDict,Dictionary,lenDict)
	listDirs = os.walk(mainDir).__next__()[1]
	gtotalReplacements = 0
	grightWords = 0
	gunReplacable = 0
	gnoCand=0
	gnoNum=0
	if not os.path.exists(outputDir):
		os.mkdir(outputDir)
	for fold in listDirs:
		listFiles = os.walk(mainDir+"/"+fold).__next__()[2]
		os.mkdir(outputDir+"/"+fold)
		for inFile in listFiles:
			with open(mainDir+"/"+fold+"/"+inFile,'r') as f, open(outputDir + "/" + fold+ "/" +inFile,'a') as o:
				for line in f:
					for words in line.split():
						Candit=[]
						testlist=[]
						if not is_number(words.strip()):
							for item in words.strip():
								testlist.append(item)
							Candit=DictSearch(testlist)
							#print("Candidate search time in s")
							#Candit=timeof(DictSearch,testlist)
							print(len(Candit))
							print(Candit)
							#print(words)
							if len(Candit)==1:
								o.write(''.join(Candit)+' ')
								grightWords+=1
							else:
								if Candit:
									obj=[]
									#print("Time for findLeven")
									d,obj=findLeven(Candit,words,obj)
									#d=timeof(findLeven,Candit,words,obj)
									tolerance=int(float(len(words.strip()))*0.5)+1
									if d<=tolerance:
										o.write(''.join(obj)+' ')
										if d==0:
											grightWords+=1
										else:
											gtotalReplacements+=1
									else:
										o.write(words+' ')
										gunReplacable+=1
								else:
									o.write(words+' ')
									gnoCand+=1
						else:
							o.write(words+' ')
							gnoNum+=1						
					o.write("\n")
					o.flush()
if not os.path.exists(sys.argv[5]):
	os.mkdir(sys.argv[5])
with open(sys.argv[5]+'/'+sys.argv[5],'w+') as stat:
	stat.write("Total replacements = " + str(gtotalReplacements)+'\n')
	stat.write("Right words = " + str(grightWords)+'\n')
	stat.write("Unreplacable = " + str(gunReplacable+gnoCand)+'\n')
	stat.write("Numbers = " + str(gnoNum)+'\n')
