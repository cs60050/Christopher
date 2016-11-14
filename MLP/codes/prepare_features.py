##############################################################
# Functions for extracting the context and mention features  #
##############################################################

import cPickle as pkl
import glob
import numpy as np
from nltk.parse.stanford import StanfordDependencyParser
import nltk

path_to_jar = "../stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0.jar"
path_to_models_jar = "../stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0-models.jar"
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

# Creating a vector for non vocabulary words
emptyVec = []
for i in range(300):
	emptyVec.append(0)
emptyVec = np.asarray(emptyVec, dtype='float32')

def subfinder(mylist, pattern):
    matches = []
    for i in range(len(mylist)):
        if mylist[i] == pattern[0] and mylist[i:i+len(pattern)] == pattern:
            matches.append(i)
    return matches

# Create avg of all word vectors for all mentions in a file
def createAvgWordVector(fname):
	ids = pkl.load(open("../data/mentions/indexed/" + fname + ".p",'r'))
	vectors = pkl.load(open("../data/word_vectors/" + fname + ".p",'r'))
	mentions = pkl.load(open("../data/mentions/" + fname + ".p",'r'))
	vec = {}
	for Id in ids.keys():
		if Id not in vec.keys():
			mention = ids[Id].split()
			avg = []
			for i in range(300):
				val = 0
				for word in mention:
					if word in vectors.keys():
						val = val + vectors[word][i]
				val = val/300
				avg.append(val)
			for mId in mentions[ids[Id]]:
				vec[mId] = avg
	pkl.dump(vec,open("../data/features/avg_word_vectors/"+fname+".p",'w'))

# Get the head word of a mention (first noun/pronoun)
def getHeadWord(mention):
	tag = nltk.pos_tag(mention.split())
	for t in tag:
		if t[1] == 'PRP' or	 t[1] == 'NN' or t[1] == 'NNP' or t[1] == "NNS" or t[1] == "NNPS":
			return t[0]
	return mention.split()[0]

# Create first, head, last word vectors of a mention
def createFHLWordVector(fname):
	ids = pkl.load(open("../data/mentions/indexed/" + fname + ".p",'r'))
	vectors = pkl.load(open("../data/word_vectors/" + fname + ".p",'r'))
	mentions = pkl.load(open("../data/mentions/" + fname + ".p",'r'))
	vec = {}
	for Id in ids.keys():
		if Id not in vec.keys():
			mention = ids[Id]
			head = getHeadWord(mention)
			mention = ids[Id].split()
			f = emptyVec
			h = emptyVec
			l = emptyVec
			fhl = []
			if mention[0] in vectors.keys():
				f = vectors[mention[0]]
			if head in vectors.keys():
				h = vectors[head]
			if mention[-1] in vectors.keys():
				l = vectors[mention[-1]]
			fhl = f.tolist() + h.tolist() + l.tolist()
			for mId in mentions[ids[Id]]:
				vec[mId] = fhl
	pkl.dump(vec,open("../data/features/fhl_word_vectors/"+fname+".p",'w'))

# Create average of context word vectors of a mention
def createContextWordVector(fname):
	ids = pkl.load(open("../data/mentions/indexed/" + fname + ".p",'r'))
	vectors = pkl.load(open("../data/word_vectors/" + fname + ".p",'r'))
	mentions = pkl.load(open("../data/mentions/" + fname + ".p",'r'))
	text = open("../data/textwo/" + fname + ".txt",'r').read().split()
	vec = {}
	for Id in ids.keys():
		mention = ids[Id]
		rep = subfinder(mentions[mention],[Id])
		mention = mention.split()
		match = subfinder(text,mention)
		wv = emptyVec.tolist()
		if rep[0] >= len(match):
			vec[Id] = wv
			continue
		pos = match[rep[0]]
		for i in range(300):
			if pos > 0 and text[pos-1] in vectors.keys():
				wv[i] = wv[i] + vectors[text[pos-1]].tolist()[i]
			if pos > 1 and text[pos-2] in vectors.keys():
				wv[i] = wv[i] + vectors[text[pos-2]].tolist()[i]
			if pos < len(text)-len(mention)-1 and text[pos+len(mention)+1] in vectors.keys():
				wv[i] = wv[i] + vectors[text[pos+len(mention)+1]].tolist()[i]
			if pos < len(text)-len(mention)-2 and text[pos+len(mention)+2] in vectors.keys():
				wv[i] = wv[i] + vectors[text[pos+len(mention)+2]].tolist()[i]
			wv[i] = wv[i]/4
		vec[Id] = wv
	pkl.dump(vec,open("../data/features/context_word_vectors/"+fname+".p",'w'))


# Get the dependency b/w headword and its parent in a mention
def getHeadDependency(fname):
	ids = pkl.load(open("../data/mentions/indexed/" + fname + ".p",'r'))
	mentions = pkl.load(open("../data/mentions/" + fname + ".p",'r'))
	text = open("../data/textwo/" + fname + ".txt",'r').read().replace('/','').split()
	vec = {}
	for Id in ids.keys():
		mention = ids[Id]
		rep = subfinder(mentions[mention],[Id])
		mentionSp = mention.split()
		match = subfinder(text,mentionSp)
		rel = "null"
		if rep[0] >= len(match):
			vec[Id] = rel
			continue
		pos = match[rep[0]]
		if len(mention.split()) > 1 :
			start = pos
			while text[start-1] != '.' and text[start-1] != '?' and text[start-1] != '!' and start>1:
				start = start - 1
			line = ""
			while text[start]!='.' and text[start] != '?' and text[start] != '!' and text[start] != '?' and text[start] != '!' and start<len(text)-1:
				line = line + " " + text[start]
				start = start + 1
			line = line + " " + text[start]
			result = dependency_parser.raw_parse(line)
			dep = result.next()
			res = list(dep.triples())
			head = getHeadWord(mention)
			for d in res:
				if d[2][0] == head:
					rel = d[1]
					break
		vec[Id] = rel
	pkl.dump(vec,open("../data/features/head_dep/"+fname+".p",'w'))

# Getting all file names
files = glob.glob("../data/coref_data/*")

# Run on all files
for fname in files:
	print "Creating for " + fname
	fname = fname.split('/')[-1]
	fname = fname.split('.')[0]

	createAvgWordVector(fname)
	getHeadDependency(fname)
	createFHLWordVector(fname)
	createContextWordVector(fname)