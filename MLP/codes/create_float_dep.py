########################################################
# Save interger dependency feature to particular file  #
########################################################

import cPickle as pkl
import glob

def createFloatDep(fname):
	dep_values = pkl.load(open("../data/features/head_dep/" + fname,'r'))
	dep_indices = pkl.load(open("../data/features/head_dep/dict/dep_dict.p",'r'))

	num_vals = {}

	for key in dep_values.keys():
		num_vals[key] = dep_indices[dep_values[key]]

	pkl.dump(num_vals, open("../data/features/head_dep/number/" + fname,'w'))

files = glob.glob("../data/features/head_dep/*.p")

for fname in files:
	fname = fname.split('/')[-1]
	print fname
	createFloatDep(fname)