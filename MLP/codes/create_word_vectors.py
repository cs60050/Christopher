####################################################
# Creating word vectors of the words in the files  #
####################################################

import gensim
import glob
import numpy as np
import cPickle as pkl

# Word2Vec model
model = gensim.models.Word2Vec.load_word2vec_format('../data/GoogleNews-vectors-negative300.bin', binary=True)

# Input files
inputDir = "../data/text/"
files = glob.glob(inputDir + "*")

# Creating a vector for non vocabulary words
emptyVec = []
for i in range(300):
	emptyVec.append(0)
emptyVec = np.asarray(emptyVec, dtype='float32')

# Creating word vectors of all words in a file
def createVectors(fname):
	text = open(fname,'r').read()
	words = text.split()
	vectors = {}
	for word in words:
		if word not in vectors.keys():
			if word not in model.vocab.keys():
				vectors[word] = emptyVec
			else:
				vectors[word] = model[word]
	fname = fname.split('/')[-1]
	fname = fname.split('.')[0]
	outputFile = open("../data/word_vectors/" + fname + ".p",'w')
	pkl.dump(vectors,outputFile)
	vectors = {}

# Run for all files
for fname in files:	
	print fname
	createVectors(fname)


