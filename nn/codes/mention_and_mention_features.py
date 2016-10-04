################################################
# Final mention and mention feature functions  #
################################################

import pickle

def generateFeatures(fname):
	def getDistance(id1,id2):
		dictList = pickle.load(open("../data/pickleFiles/"+fname+".p"))
		fmention = None
		smention = None
		fcount = -1
		scount = -1
		for key in dictList :
			if id1 in dictList[key] and fcount == -1:
				fmention = key
				fcount = dictList[key].index(id1) + 1
				break
		for key in dictList :
			if id2 in dictList[key] and scount == -1:
				smention = key
				scount = dictList[key].index(id2) + 1
				break
		text = open("../data/text/"+fname+".txt","r")	
		line1 = 0
		line2 = 0
		for line in text :
			textsplit = line
		textsplit = sent_tokenize(textsplit)
		count  = 0
		linediff = 0
		for i in range(len(textsplit)):
			if fmention in textsplit[i]  : 
				count += 1
				if count == fcount :
					linediff = i+1
					break
		count = 0
		for i in range(len(textsplit)):
			if smention in textsplit[i]  : 
				count += 1
				if count == scount :
					linediff -= i+1
					break
		intermentions = abs(id1-id2)
		return abs(linediff) , intermentions

	def mentionMatch(id1,id2):
		dictList = pickle.load(open("../data/pickleFiles/"+fname+".p"))
		fmention = None
		smention = None
		scount = -1
		fcount = -1
		for key in dictList :
			if id1 in dictList[key] and fcount == -1:
				fmention = key
				break
		for key in dictList :
			if id2 in dictList[key] and scount == -1:
				smention = key
				break
		if fmention == smention :
			return 1
		elif fmention in smention or smention in fmention :
			return 0
		else :
			return -1

	def headMatch(id1,id2):
		dictList = pickle.load(open("../data/pickleFiles/"+fname+".p"))
		fmention = None
		smention = None
		scount = -1
		fcount = -1
		for key in dictList :
			if id1 in dictList[key] and fcount == -1:
				fmention = key
				break
		for key in dictList :
			if id2 in dictList[key] and scount == -1:
				smention = key
				break
		wd1 = word_tokenize(fmention)
		wd2 = word_tokenize(smention)
		tg1 = pos_tag(wd1)
		tg2 = pos_tag(wd2)
		head1 = None
		head2 = None
		for i in tg1 :
			if i[1] == "NN" or i[1] =="NNS" or i[1] == "NNP" or i[1] == "NNPS" or i[1] == "PRP" or i[1] == "PRP$":
				head1 = i[0]
				break
		for i in tg2 :
			if i[1] == "NN" or i[1] =="NNS" or i[1] == "NNP" or i[1] == "NNPS" or i[1] == "PRP" or i[1] == "PRP$":
				head2 = i[0]
				break
		if head1 == head2 :
			return 1
		else :
			return -1
	


	