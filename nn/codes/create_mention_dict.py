###################################################################
# Getting the entire text from xml                                #
# Creating a dict mapping mentions to a list of respective ids    #
# Creating a dict mapping ids to their respective mentions        #
###################################################################

import xml.etree.ElementTree as et
import glob
import cPickle as pkl
import re

files = glob.glob("../data/coref_data/*")

mentions = {}
mId = 0

# Get the text inside a tag (fully formatted)
def getText(tag):
	text = ""
	if tag.text != None:
		text = tag.text
	for child in tag:
		text = text + getText(child)
		if child.tail !=None:
			text = text + child.tail
	text = text.replace('\t',' ')
	text = text.replace('\n',' ')
	text = text.replace(' \'','\'')
	text = re.sub(' +',' ',text)
	return text.strip()

# Get the text inside a tag (non formatted)
def getTextwo(tag):
	text = ""
	if tag.text != None:
		text = " " + tag.text.replace(' \'','\'')
	for child in tag:
		text = text + getTextwo(child)
		if child.tail !=None:
			text = text + " " + child.tail.replace(' \'','\'')
	text = text.replace('\t',' ')
	# text = text.replace('\n',' ')
	text = re.sub(' +',' ',text)
	return text.strip()

# Create a dict for mapping mentions to a list of ids
def prepareMentions(tag,mId):
	if tag.tag == 'COREF':
		text = getText(tag)	
		if text in mentions.keys():
			mentions[text].append(mId)
		else:
			a = []
			a.append(mId)
			mentions[text] = a
		mId = mId + 1
	for child in tag:
		mId = prepareMentions(child,mId)

	return mId

# Create a dict mapping id to mention
def prepareDict(fname):
	d = {}
	for mention in mentions.keys():
		for ind in mentions[mention]:
			d[ind] = mention
	outputFile = open("../data/mentions/indexed/" + fname + ".p", 'w')
	pkl.dump(d,outputFile)

# Run for all files
for fname in files:
	print "Creating mentions for " + fname
	tree = et.parse(fname)
	root = tree.getroot()
	prepareMentions(root,0)

	fname = fname.split('/')[-1]
	fname = fname.split('.')[0]
	
	oname = "../data/mentions/" +fname +".p"
	output = open(oname,'w')
	pkl.dump(mentions,output)
	
	oname = "../data/text/" +fname +".txt"
	output = open(oname,'w')
	output.write(getText(root))

	oname = "../data/textwo/" +fname +".txt"
	output = open(oname,'w')
	output.write(getTextwo(root))
	
	prepareDict(fname)

	mentions = {}

