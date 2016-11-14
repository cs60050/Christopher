##########################################
# Mapping dependency labels to integers  #
##########################################

import cPickle as pkl
import glob

dep_dict = {}

def depToFloat(fname,ind):
	dep_values = pkl.load(open(fname,'r'))
	for key in dep_values.keys():
		if dep_values[key] not in dep_dict.keys():
			dep_dict[dep_values[key]] = ind
			ind = ind + 1
	return ind

files = glob.glob("../data/features/head_dep/*")

i = 0

for fname in files:
	if fname.split('.')[-1] == "p":
		i = depToFloat(fname, i)

pkl.dump(dep_dict, open("../data/features/head_dep/dict/dep_dict.p",'w'))

