from gensim.models import Word2Vec
# import extractors.tokenizer as tokenizer
#import tokenizer
import numpy as np
import os
import glob
import pickle as pkl


basepath = ""
datapath = basepath

articles = ['a', 'an', 'the']

def possible_head_nouns(mentionText):
    mentionText = mentionText.lower().strip()
    mentionText = mentionText.split(' , ')[0]
    relative_pronouns = [' who ', ' that ', ' which ', ' whichever ', ' whoever ', ' whom ', 'whomever ']
    prepositions = [" aboard ", " about ", " above ", " across ", " after ", " against ", " along ", " alongside ", " amid ", " among ", " amongst ", " around ", " as ", " aside ", " astride ", " at ", " atop ", " barring ", " before ", " behind ", " below ", " beneath ", " beside ", " besides ", " between ", " beyond ", " but ", " by ", " circa ", " concerning ", " considering ", " despite ", " down ", " during ", " except ", " excepting ", " excluding ", " failing ", " following ", " for ", " from ", " in ", " including ", " inside ", " into ", " like ", " minus ", " near ", " nearby ", " next ", " notwithstanding ", " of ", " off ", " on ", " onto ", " opposite ", " outside ", " over ", " past ", " per ", " plus ", " regarding ", " round ", " save ", " since ", " than ", " through ", " throughout ", " till ", " times ", " to ", " toward ", " towards ", " under ", " underneath ", " unlike ", " until ", " unto ", " up ", " upon ", " versus ", " via ", " with ", " within ", " without ", " worth "]
    for relative_pronoun in relative_pronouns:
        mentionText = mentionText.split(relative_pronoun)[0].strip()
    for preposition in prepositions:
        mentionText = mentionText.split(preposition)[0].strip()
    mentionText = [word for word in mentionText.split(' ') if (word not in articles)]
    # print ' '.join(mentionText).strip()
    return mentionText

def get_stopwords(filename):
    words = open(filename, "r")
    return [ word.strip() for word in words.readlines()]

model = None
stopwords = get_stopwords(os.path.join(datapath, "stopwords.txt"))

NDIM = 300
def embedding(text):
	global model
	if(model is None):
		model = Word2Vec.load_word2vec_format('google_news_300.bin', binary=True)
	# parsed = tokenizer.parse(text.strip())
	# embeds = []
	# for sentence in parsed:
	# 	toks = sentence['tokens']
	# 	for tokeninfo in toks:
	# 		if tokeninfo['word'].lower() in stopwords:
	# 			continue
	# 		try:
	# 			word = tokeninfo['word'].lower()
	# 			embeds.append(model[word])
	# 		except:
	# 			try:
	# 				embeds.append(model[tokeninfo['lemma']].lower())
	# 			except:
	# 				pass
	
	embeds = []
	# # text = ' '.join(possible_head_nouns(text)).strip()
	# try:
	# 	# embeds.append(model[text])
	# 	embeds = model[text]
	# 	if len(text.split(' '))>1:
	# 		print '####### Could Embed', text
	# except:
	# 	# try:
	# 	# 	embeds.append(model[tokeninfo['lemma']].lower())
	# 	# except:
	# 	# 	pass
	# 	print "Could not Embed :", text


	# embeds = np.asarray(embeds)
	# return embeds

	text = possible_head_nouns(text)
	try:
		for word in text:
			try:
				embWord = model[word]
			except:
				embWord = [0]*300
			embeds.append(embWord)
			# embeds = model[text]
	except:
		# try:
		# 	embeds.append(model[tokeninfo['lemma']].lower())
		# except:
		# 	pass
		print "Could not Embed :", text
	if len(embeds) == 0:
		print '################################ Embeds is', embeds
		embeds = [[0]*300]
	embeds = np.asarray(embeds)
	return np.mean(embeds, axis=0)

def feature_names():
	return ["embed_"+str(i) for i in range(NDIM)]


def sentence_sim(sent1, sent2):
	global model
	if(model is None):
		print 'Loading model'
		model = Word2Vec.load_word2vec_format('embeddings/google_news_300.bin', binary=True)
		print 'Loaded model'
	parsed = tokenizer.parse(sent1.strip())
	sent1_ = [tokeninfo['word'] for sentence in parsed 
		for tokeninfo in sentence['tokens'] if tokeninfo['word'] not in stopwords]
	parsed = tokenizer.parse(sent2.strip())
	sent2_ = [tokeninfo['word'] for sentence in parsed 
		for tokeninfo in sentence['tokens'] if tokeninfo['word'] not in stopwords]

	return  model.wmdistance(sent1_, sent2_)

def main_for_embedding():
    directory = '/home/priyank/Desktop/7thSem/ML_Project/data/mentionsWithMayBeSubject/'
    pickle_directory = '/home/priyank/Desktop/7thSem/ML_Project/codes_new/pickles_new/'
    files = glob.glob(directory+"*")
    num_files_done = 0
    for fname in files:
        print 'Doing for file -', fname, num_files_done+1, 'of', len(files)
        print
        mentionDictionary = pkl.load(open(fname,'rb'))#load_dict(fname)
        keys = sorted(mentionDictionary.keys())
        classes = {}
        for i in range(len(keys)):
            print i, 'of', len(keys)
            mention = mentionDictionary[keys[i]]
            emb = embedding(mention['MENTION'])
            # classes[mention['MENTION']] = klass,score
            # print mention['MENTION'], klass, score
        # pkl.dump(classes,open(pickle_directory+fname.split('.')[0].split('/')[-1]+'_embeds.p','wb'))

if __name__ == '__main__':
	main_for_embedding()