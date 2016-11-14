import pickle 
from nltk import sent_tokenize
from nltk import pos_tag
from nltk import word_tokenize
import os
import pickle

pDir = "../data/dataSet/"
pFiles = os.listdir(pDir)

for file in pFiles :
	print file
	filedict  = pickle.load(open(pDir + file))
	idOut = pickle.load(open("../data/mentionID/" + file))
	y_train = list()
	for val in filedict :
		if idOut[val[0]] == idOut[val[1]] :
			y_train.append([val,1])
		else :
			y_train.append([val,0])

	pickle.dump(y_train,open("../data/y_train/"+file,"w"))
	print "Done with File"