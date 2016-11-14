import pickle 
from nltk import sent_tokenize
from nltk import pos_tag
from nltk import word_tokenize
import os

def createData(fname):
	avgFile = pickle.load(open("../data/features/avg_word_vectors/" + fname + ".p",'r'))
	fhlFile = pickle.load(open("../data/features/fhl_word_vectors/" + fname + ".p",'r'))
	contextFile = pickle.load(open("../data/features/context_word_vectors/" + fname + ".p",'r'))
	depFile = pickle.load(open("../data/features/head_dep/number/" + fname + ".p",'r'))
	menFile = pickle.load(open("../data/mentionPairs/"+fname+".p","r"))
	def avgWordVector(mId):
		return avgFile[mId]

	def fhlWordVector(mId):
		return fhlFile[mId]

	def contextWordVector(mId):
		return contextFile[mId]

	def headDep(mId):
		return depFile[mId]		

	def getPairwiseFeatureValues(mId1,mId2):
		if mId1 == mId2 :
			return [0,0,1,1]
		mId1,mId2 = min(mId1,mId2),max(mId1,mId2)
		return menFile[(mId1,mId2)]


	dictList = pickle.load(open("../data/mentions/"+fname+".p"))
	maxi = -1
	valList = {}
	for key in dictList :
		# print dictList[key]
		for i in dictList[key] :
			maxi = max(maxi,i)

	# print maxi, fname
	for i in xrange(maxi+1):
		for j in xrange(i+1,maxi+1):
			mValues = getPairwiseFeatureValues(i,j)
			valList[(i,j)] = [avgWordVector(i),avgWordVector(j),fhlWordVector(i),fhlWordVector(j),contextWordVector(i),contextWordVector(j),headDep(i),headDep(j),getPairwiseFeatureValues(i,j)]
	# print valList
	#coun = 0
	#for key in valList.keys():
	#    for i in valList[key] :
	#	print i, 
	#    print 
	#    coun += 1
	#    if coun == 5 :
	#	break
	pickle.dump(valList,open("../data/dataSet/"+fname+".p","w"))
	return 

pickDir = "../data/mentions/"
datasets = os.listdir(pickDir)
for data in datasets :
	s = data
	print s
	if s[-2] == '.' :
		createData(s[:-2])
		#break
