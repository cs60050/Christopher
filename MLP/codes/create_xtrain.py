import pickle 
from nltk import sent_tokenize
from nltk import pos_tag
from nltk import word_tokenize
import os

pDir = "../data/dataSet/"
pFiles = os.listdir(pDir)



for file in pFiles :
	filedict  = pickle.load(open(pDir + file))
	x_train = list()
	for val in filedict :
		temp = list()
		for obj in filedict[val]:
			if isinstance(obj,list) == True :
				temp += obj
			else :
				temp.append(obj)
		# print len(temp)
		x_train.append(temp) 
	print len(x_train)
	pickle.dump(x_train,open("../data/x_train/" + file,"w"))