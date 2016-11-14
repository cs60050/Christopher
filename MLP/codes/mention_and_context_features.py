################################################
# Final mention and context feature functions  #
################################################

import cPickle as pkl

def generateFeatures(fname):
	avgFile = pkl.load(open("../data/features/avg_word_vectors/" + fname + ".p",'r'))
	fhlFile = pkl.load(open("../data/features/fhl_word_vectors/" + fname + ".p",'r'))
	contextFile = pkl.load(open("../data/features/context_word_vectors/" + fname + ".p",'r'))
	depFile = pkl.load(open("../data/features/head_dep/number/" + fname + ".p",'r'))

	def avgWordVector(mId):
		return avgFile[mId].tolist()

	def fhlWordVector(mId):
		return fhlFile[mId]

	def contextWordVector(mId):
		return contextFile[mId]

	def headDep(mId):
		return depFile[mId]		
