import cPickle as pkl

# from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

import glob
from time import time

############################################################# SOME COLLECTIONS #########################################################################
subject_pronouns = ['i', 'you', 'he', 'she', 'it', 'they', 'we']
object_pronouns = ['me', 'you', 'him', 'her', 'it', 'us', 'them']
possesive_pronouns = ['mine', 'his', 'hers', 'its', 'ours', 'yours', 'their', 'theirs']
intensive_or_reflexive_pronouns = ['myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'yourselves', 'themselves']
demontrative_pronouns = ['this', 'these', 'those', 'that']

articles = ['a', 'an', 'the']

singular_pronouns = ['I','me','she','her','he','him','it','this','that','myself','yourself','himself','herself','itself','my','his','its','mine','hers']
plural_pronouns = ['we','us','they','them','these','those','ourselves','themselves','yourselves','our','their','ours','theirs']
########################################################################################################################################################

# country_list = ["America", "UK", "Afghanistan", "Albania", "Algeria", "Samoa", "Andorra", "Angola", "Anguilla", "Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Botswana", "Island", "Brazil", "Brunei", "Bulgaria", "Burundi", "Cambodia", "Cameroon", "Canada", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Croatia", "Cuba", "Cyprus", "Denmark", "Djibouti", "Timor", "Ecuador", "Egypt", "Salvador", "Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea", "Kuwait", "Kyrgyzstan", "Latvia", "Lebanon", "Lesotho"]
#NOTE : We need to make them lower case

# location_identifiers = ['Samoa','London','city','country','nation','location','district','state','province']

organization_identifiers = ['corp', 'inc.', 'corporations', 'department','research','school','college','university','center', 'institute', 'technologies', 'pvt.', 'ltd.', 'congress','league','house','commission','committie','party']
# NOTE : Many organizations start with 'the', while no country or person name does! Use this, along with upper cases, to find organizations.

datetime_identifiers = ['date', 'time','today', 'tomorrow', 'yesterday', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'now']

person_identifiers = ['i', 'you', 'he', 'she', 'they', 'we', 'me', 'him', 'us', 'them','mine', 'his', 'her', 'hers', 'their', 'theirs', 'myself', 'yourself', 'himself', 'herself', 'ourselves', 'yourselves', 'themselves','man','woman','person','lady','gentleman','women','men','people','gentlemen']
non_person_identifiers = ['it', 'itself']
########################################################################################################################################################

def load_dict(filename):
    return pkl.load(open(filename,'rw'))

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


def init():
    global location_synsets
    global organization_synsets
    global person_synsets
    global date_time_synsets
    print 'Initializing...'
    location_synsets_string = ['topographic_point.n.01', 'place.n.02', 'area.n.01', 'city.n.01', 'country.n.02', 'location.n.01']
    # organization_synsets_string = ['association.n.01', 'organization.n.01', 'corporation.n.01', 'department.n.01', 'institute.n.01', 'company.n.01', 'committee.n.01']
    organization_synsets_string = ['organization.n.01', 'corporation.n.01', 'company.n.01']
    person_synsets_string = ['person.n.01', 'man.n.01', 'woman.n.01']
    date_time_synsets_string = ['date.n.01', 'clock_time.n.01','today.n.02', 'tomorrow.n.01', 'yesterday.n.01', 'january.n.01', 'now.n.01']
    for location_synset_string in location_synsets_string:
        location_synsets.append(wordnet.synset(location_synset_string))
    for organization_synset_string in organization_synsets_string:
        organization_synsets.append(wordnet.synset(organization_synset_string))
    for person_synset_string in person_synsets_string:
        person_synsets.append(wordnet.synset(person_synset_string))
    for date_time_synset_string in date_time_synsets_string:
        date_time_synsets.append(wordnet.synset(date_time_synset_string))

def find_class_score(words, classSynsets):
    # classSynsets = []
    # for synset_string in classSynsetsString:
    #     classSynsets.append(wordnet.synset(synset_string))

    # t4 = time()
    maxSimilarity = 0
    maxAvgSimilarity = 0
    for word in words:
        synsets = wordnet.synsets(word)
        for word_synset in synsets:
            avgSimilarity = 0
            for class_synset in classSynsets:
                similarity = word_synset.wup_similarity(class_synset)
                if similarity == None:
                    similarity = 0
                avgSimilarity += similarity
                # if similarity>maxSimilarity:
                #     maxSimilarity = max(maxSimilarity,similarity)
            avgSimilarity/=len(classSynsets)
            maxAvgSimilarity = max(maxAvgSimilarity,avgSimilarity)    
    # t5 = time()
    # print '***', (t5-t4)*1000
    return maxAvgSimilarity

def location_class(words):
    # location_synsets_string = ['topographic_point.n.01', 'place.n.02', 'area.n.01', 'city.n.01', 'country.n.02', 'location.n.01']
    # print len(location_synsets)
    return find_class_score(words, location_synsets)

def organization_class(words):
    # organization_synsets_string = ['association.n.01', 'organization.n.01', 'corporation.n.01', 'department.n.01', 'institute.n.01', 'company.n.01', 'committee.n.01']
    # organization_synsets_string = ['organization.n.01', 'corporation.n.01', 'company.n.01']
    return find_class_score(words, organization_synsets)

def person_class(words):
    # pass
    # person_synsets_string = ['person.n.01', 'man.n.01', 'woman.n.01']
    return find_class_score(words, person_synsets)

def date_time_class(words):

    # date_time_synsets_string = ['date.n.01', 'clock_time.n.01','today.n.02', 'tomorrow.n.01', 'yesterday.n.01', 'january.n.01', 'now.n.01']
    return find_class_score(words,date_time_synsets)

LOCATION = 'LOCATION'
ORGANIZATION = 'ORGANIZATION'
PERSON = 'PERSON'
# wnl = WordNetLemmatizer()


def semantic_class(mention):
    # t6 = time()
    words = possible_head_nouns(mention['MENTION'])
    # t7 = time()
    # print '///', (t7-t6)*1000
    # words = [word.replace("'s","") for word in words if word not in person_identifiers]
    words = [word.replace("'s","") for word in words]
    # if words[-1] in person_identifiers:
    #     return PERSON, 1
    Words = words[:]
    words = []
    if len(Words)>0:
        words.append(Words[-1])
    else:
        return PERSON, -1
    locationScore = location_class(words)
    organizationScore = organization_class(words)
    personScore = person_class(words)
    dateTimeScore = date_time_class(words)
    score = -1
    klass = None
    if locationScore > score:
        score = locationScore
        klass = LOCATION
    if organizationScore > score:
        score = organizationScore
        klass = ORGANIZATION
    if personScore > score:
        score = personScore
        klass = PERSON
    if dateTimeScore > score:
        score = dateTimeScore
        klass = 'DATETIME'
    if score >=0  and score < 0.55:
        klass = 'UNKNOWN'
    return klass,score
    

def main_for_semantic():
    directory = '/home/priyank/Desktop/7thSem/ML_Project/data/mentionsWithMayBeSubject/'
    pickle_directory = '/home/priyank/Desktop/7thSem/ML_Project/codes_new/pickles/'
    files = glob.glob(directory+"*")
    num_files_done = 0
    for fname in files:
        print 'Doing for file -', fname, num_files_done+1, 'of', len(files)
        print
        mentionDictionary = load_dict(fname)
        keys = sorted(mentionDictionary.keys())
        classes = {}
        for i in range(len(keys)):
            print i, 'of', len(keys)
            mention = mentionDictionary[keys[i]]
            klass,score = semantic_class(mention)
            classes[mention['MENTION']] = klass,score
            # print mention['MENTION'], klass, score
        pkl.dump(classes,open(pickle_directory+fname.split('.')[0].split('/')[-1]+'_classes.p','wb'))
            
location_synsets = []
organization_synsets = []
person_synsets = []
date_time_synsets = []
init()
# main_for_semantic()
