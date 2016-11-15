import cPickle as pkl
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize

import find_class
import wordToVec

wnl = WordNetLemmatizer()

############################################################# SOME COLLECTIONS #########################################################################
subject_pronouns = ['i', 'you', 'he', 'she', 'it', 'they', 'we']
object_pronouns = ['me', 'you', 'him', 'her', 'it', 'us', 'them']
possesive_pronouns = ['mine', 'his', 'hers', 'its', 'ours', 'yours', 'their', 'theirs']
intensive_or_reflexive_pronouns = ['myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'yourselves', 'themselves']
demontrative_pronouns = ['this', 'these', 'those', 'that']

articles = ['a', 'an', 'the']

# singular_pronouns = ['I','me','she','her','he','him','it','this','that','myself','yourself','himself','herself','itself','my','his','its','mine','hers']
# plural_pronouns = ['we','us','they','them','these','those','ourselves','themselves','yourselves','our','their','ours','theirs']
########################################################################################################################################################

# country_list = ["America", "UK", "Afghanistan", "Albania", "Algeria", "Samoa", "Andorra", "Angola", "Anguilla", "Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Botswana", "Island", "Brazil", "Brunei", "Bulgaria", "Burundi", "Cambodia", "Cameroon", "Canada", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Croatia", "Cuba", "Cyprus", "Denmark", "Djibouti", "Timor", "Ecuador", "Egypt", "Salvador", "Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea", "Kuwait", "Kyrgyzstan", "Latvia", "Lebanon", "Lesotho"]
#NOTE : We need to make them lower case

# location_identifiers = ['Samoa','London','city','country','nation','location','district','state','province']

organization_identifiers = ['corp', 'inc.', 'corporations', 'department','research','school','college','university','center', 'institute', 'technologies', 'pvt.', 'ltd.', 'congress','league','house','commission','committie','party']
# NOTE : Many organizations start with 'the', while no country or person name does! Use this, along with upper cases, to find organizations.

datetime_identifiers = ['today', 'tomorrow', 'yesterday', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'now']

# person_identifiers = ['i', 'you', 'he', 'she', 'they', 'we', 'me', 'him', 'us', 'them','mine', 'his', 'hers', 'their', 'theirs', 'myself', 'yourself', 'himself', 'herself', 'ourselves', 'yourselves', 'themselves','man','woman','person','lady','gentleman','women','men','people','gentlemen']
# non_person_identifiers = ['it', 'itself']
########################################################################################################################################################


singular_pronouns = ['I','me','she','her','he','him','it','this','that','myself','yourself','himself','herself','itself','my','his','its','mine','hers']
plural_pronouns = ['we','us','they','them','these','those','ourselves','themselves','yourselves','our','their','ours','theirs']

person_identifiers = ['i', 'you', 'he', 'she', 'they', 'we', 'me', 'him', 'us', 'them','mine', 'his', 'hers', 'their', 'theirs', 'myself', 'yourself', 'himself', 'herself', 'ourselves', 'yourselves', 'themselves','man','woman','person','lady','gentleman','women','men','people','gentlemen']
non_person_identifiers = ['it', 'itself']

def load_dict(filename):
    return pkl.load(open(filename,'rw'))

def We_Should_Consider(mention1,mention2):
    mention1 = mention1['MENTION'].lower().strip()
    mention2 = mention2['MENTION'].lower().strip()
    if (mention1 in person_identifiers and mention2 in non_person_identifiers) or (mention1 in non_person_identifiers and mention2 in person_identifiers):
        return False
    if (mention1 in singular_pronouns and mention2 in plural_pronouns) or (mention1 in plural_pronouns and mention2 in singular_pronouns):
        return False
    return True


def consecutiveSubjects(mention1, mention2):
    return abs(mention2['SENT_NUM'] - mention1['SENT_NUM'])==1 and mention1['MAY_BE_SUBJECT'] and mention2['MAY_BE_SUBJECT']

def isPronoun(mention): 
    NOT_A_PRONOUN = 0
    SUBJECT_PRONOUN = 1
    OBJECT_PRONOUN = 2
    POSSESIVE_PRONOUN = 3
    INT_OR_REFLEX_PRONOUN = 4

    mention = mention['MENTION'].lower().strip()
    if mention in subject_pronouns:
        return SUBJECT_PRONOUN
    if mention in object_pronouns:
        return OBJECT_PRONOUN
    if mention in possesive_pronouns:
        return POSSESIVE_PRONOUN
    if mention in intensive_or_reflexive_pronouns:
        return INT_OR_REFLEX_PRONOUN
    else:
        return NOT_A_PRONOUN
    
def match(mention1,mention2):
    
    mention1 = mention1['MENTION'].lower().strip()
    mention2 = mention2['MENTION'].lower().strip()
    mention1 = [word for word in mention1.split() if (word not in articles) and (word not in demontrative_pronouns)]
    mention2 = [word for word in mention2.split() if (word not in articles) and (word not in demontrative_pronouns)]
    return mention1==mention2


def definite_noun_phrase(mention1, mention2):
    mention2 = mention2['MENTION'].lower().strip()
    if mention2.split(' ')[0] == 'the':
        return 1
    else:
        return 0

def demonstrative_noun_phrase(mention):
    
    mention = mention['MENTION'].lower().strip()
    first_word = mention.split(' ')[0]
    return first_word in demontrative_pronouns

def number_agreement(mention1, mention2):
    UNKNOWN = 0
    SINGULAR = 1
    PLURAL = 2

    mention1 = mention1['MENTION'].lower().strip()
    mention2 = mention2['MENTION'].lower().strip()
    mention1_type = UNKNOWN
    mention2_type = UNKNOWN

    mention1_words_reversed = mention1.split(' ')
    mention1_words_reversed.reverse()
    mention2_words_reversed = mention2.split(' ')
    mention2_words_reversed.reverse()

    for word in mention1_words_reversed:
        if word in singular_pronouns:
            mention1_type = SINGULAR
        if word in plural_pronouns:
            mention1_type = PLURAL
    for word in mention2_words_reversed:
        if word in singular_pronouns:
            mention2_type = SINGULAR
        if word in plural_pronouns:
            mention2_type = PLURAL
    
    if mention1_type == UNKNOWN:
        for word in mention1.split(' '):
            if word in articles:
                continue
            if word == wnl.lemmatize(word, 'n'):
                mention1_type = SINGULAR
            else:
                mention1_type = PLURAL
            break

    if mention2_type == UNKNOWN:
        for word in mention2.split(' '):
            if word in articles:
                continue
            if word == wnl.lemmatize(word, 'n'):
                mention2_type = SINGULAR
            else:
                mention2_type = PLURAL
            break
    
    return mention1_type==mention2_type

def same_semantic_class(mention1,mention2,classes):

    c1,score1 = classes[mention1['MENTION']] 
    c2,score2 = classes[mention2['MENTION']]
    # print c1, score1
    # print c2, score2

    # c1,score1 = find_class.semantic_class(mention1)
    # c2,score2 = find_class.semantic_class(mention2)
    if c1=='UNKNOWN' and c2=='UNKNOWN':
        return -1
    # if c1=='UNKNOWN' or c2=='UNKNOWN' or c1!=c2:
    #     return 0
    if c1!=c2:
        return 0
    else:
        return 1

import math
def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    try:
        for i in range(len(v1)):
            x = v1[i]; y = v2[i]
            sumxx += x*x
            sumyy += y*y
            sumxy += x*y
    except:
        print v1, v2
        raise Exception('')
    if sumxx == 0 or sumyy == 0:
        return 0
    return sumxy/math.sqrt(sumxx*sumyy)

def embeddingConsineDistance(mention1,mention2):
    e1 = wordToVec.embedding(mention1['MENTION'])
    e2 = wordToVec.embedding(mention2['MENTION'])
    return cosine_similarity(e1,e2)

def get_feature_vector(mention1,mention2,classes):
    features = []
    # features.append(We_Should_Consider(mention1,mention2))
    # features.append(consecutiveSubjects(mention1,mention2))
    # features.append(isPronoun(mention1))
    # features.append(isPronoun(mention2))
    features.append(match(mention1,mention2))
    features.append(definite_noun_phrase(mention1,mention2))
    features.append(demonstrative_noun_phrase(mention2))
    # features.append(number_agreement(mention1,mention2))
    features.append(same_semantic_class(mention1,mention2,classes))
    features.append(embeddingConsineDistance(mention1,mention2))
    return features
