###################################################################
# Getting the entire text from xml                                #
# Creating a dict mapping mentions to a list of respective ids    #
# Creating a dict mapping ids to their respective mentions        #
###################################################################

import xml.etree.ElementTree as et
import glob
import cPickle as pkl
import re
from nltk.tokenize import sent_tokenize

directory = '../data/'

files = glob.glob(directory+"coref_data/*")

mentions = {}
mention_num = 0
firstInSentence = True

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

def prepareMentionsDictWithSentenceNumbers(tag,sentence,sentence_num):
	global mention_num
	global firstInSentence
	# print tag
	if tag.tag == 'COREF':
		if firstInSentence:
			mayBeSubject = True
		else:
			mayBeSubject = False
		firstInSentence = False
		text = getText(tag)
		mention_num += 1
		mentions[mention_num] = {'SENT_NUM':sentence_num,'MENTION':text,'SENT':sentence, 'ID':tag.attrib['ID'], 'MAY_BE_SUBJECT':firstInSentence}
	for child in tag:
		prepareMentionsDictWithSentenceNumbers(child,sentence, sentence_num)

def prepareMentionsDictWithSentence(sentence,sentence_num):
	global firstInSentence
	try:
		sentence_xml = et.fromstring('<SENTENCE>'+sentence+'</SENTENCE>')
	except Exception, e:
		# print type(e)
		if sentence.find('DOC')!=-1 and sentence.find('TEXT')!=-1:
			print('### Some problem : Can\'t parse the sentence "'+sentence+'" '+type(e))
		return
	firstInSentence = True
	prepareMentionsDictWithSentenceNumbers(sentence_xml,getText(sentence_xml),sentence_num)

def prepareMentionsBreakIntoSentences(xml_text):
	sentence_num = 0
	for sentence in xml_text.split('\n'):
		sentence_num += 1
		prepareMentionsDictWithSentence(sentence,sentence_num)

# Run for all files
for fname in files:
	mention_num = 0
	print "Creating mentions for " + fname
	with open(fname,'r') as f:
		xml_text = f.read()
	prepareMentionsBreakIntoSentences(xml_text)
	fname = fname.split('/')[-1].split('.')[0]
	pkl.dump(mentions,open(directory+'mentionsWithMayBeSubject/'+fname+'.p','wb'))
	# print mentions