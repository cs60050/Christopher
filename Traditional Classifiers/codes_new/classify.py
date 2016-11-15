from sklearn.cross_validation import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression

from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score

import features

import glob
import cPickle as pkl
import random

singular_pronouns = ['I','me','she','her','he','him','it','this','that','myself','yourself','himself','herself','itself','my','his','its','mine','hers']
plural_pronouns = ['we','us','they','them','these','those','ourselves','themselves','yourselves','our','their','ours','theirs']

person_identifiers = ['i', 'you', 'he', 'she', 'they', 'we', 'me', 'him', 'us', 'them','mine', 'his', 'hers', 'their', 'theirs', 'myself', 'yourself', 'himself', 'herself', 'ourselves', 'yourselves', 'themselves','man','woman','person','lady','gentleman','women','men','people','gentlemen']
non_person_identifiers = ['it', 'itself']

def load_dict(filename):
    return pkl.load(open(filename,'rw'))

# def We_Should_Consider(mention1,mention2):
#     mention1 = mention1['MENTION'].lower().strip()
#     mention2 = mention2['MENTION'].lower().strip()
#     if (mention1 in person_identifiers and mention2 in non_person_identifiers) or (mention1 in non_person_identifiers and mention2 in person_identifiers):
#         return False
#     if (mention1 in singular_pronouns and mention2 in plural_pronouns) or (mention1 in plural_pronouns and mention2 in singular_pronouns):
#         return False
#     return True

def load_dataset(files_directory,pickle_directory):
    files = glob.glob(files_directory+"*")
    x = []
    y = []
    rule_based_wrong_count = 0
    rule_based_correct_count = 0
    fnum=1
    try:
        raise Exception('Reload x and y')
        x = pkl.load(open(pickle_directory+'x_all.pkl','rb'))
        y = pkl.load(open(pickle_directory+'y_all.pkl','rb'))
    except:
        for fname in files:
            print 'processing file number', fnum, 'of', len(files), 'files' 
            fnum += 1
            mentionDictionary = load_dict(fname)
            classes = load_dict(pickle_directory+fname.split('/')[-1].split('.')[0]+'_classes.p')
            keys = sorted(mentionDictionary.keys())
            len_keys = len(keys)
            for i in range(len_keys):
                print i, 'of', len_keys
                for j in range(i+1,min(len_keys,i+20)):
                    mention1 = mentionDictionary[keys[i]]
                    mention2 = mentionDictionary[keys[j]]
                    x.append(features.get_feature_vector(mention1,mention2,classes))
                    if mention1['ID'] == mention2['ID']:
                        y.append(1)
                    else:
                        y.append(0)
                    # if We_Should_Consider(mention1,mention2):
                    #     x.append(features.get_feature_vector(mention1,mention2,classes))
                    #     if mention1['ID'] == mention2['ID']:
                    #         y.append(1)
                    #     else:
                    #         y.append(0)
                    # else:
                    #     if mention1['ID'] == mention2['ID']:
                    #         rule_based_wrong_count += 1
                    #     else:
                    #         rule_based_correct_count += 1
        pkl.dump(x, open(pickle_directory+'x_all.pkl','wb'))
        pkl.dump(y, open(pickle_directory+'y_all.pkl','wb'))
    # indices = {}
    # print 'Set of Values in y before sampling', set(y)
    # for t in set(y):
    #     indices[t] = [i for i in range(len(y)) if y[i] == t]
    # min_len = min([len(indices[t]) for t in indices])
    # for t in indices:
    #     indices[t] = random.sample(indices[t], min_len/3)
    # print 'Zero Valued : ', len(indices[0]), [y[i] for i in indices[0][:10]]
    # print 'One Valued  : ', len(indices[1]), [y[i] for i in indices[1][:10]]
    # indices = indices[0]+indices[1]
    # print 'indices finally', indices[:10]
    # # for i in indices:
    # #     if y[i] == 1:

    # x_train = []
    # y_train = []
    # x_test = []
    # y_test = []
    # for i in range(len(y)):
    #     if i in indices:
    #         x_train.append(x[i])
    #         y_train.append(y[i])
    #     else:
    #         x_test.append(x[i])
    #         y_test.append(y[i])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.4, random_state=42)

    print len(x_train), len(y_train), len(x_test), len(y_test)
    return x_train,y_train,x_test,y_test,rule_based_wrong_count,rule_based_correct_count

def evaluate(y_true,y_pred):
    return [accuracy_score(y_true, y_pred),
    f1_score(y_true, y_pred, average="binary"),
    #f1_score(y_true, y_pred, average='micro'),
    #f1_score(y_true, y_pred, average='macro'),
    #f1_score(y_true, y_pred, average='weighted'),
    #log_loss(y_true,y_pred),
    precision_score(y_true, y_pred, average="binary"),
    recall_score(y_true, y_pred, average="binary"),
    roc_auc_score(y_true, y_pred)]

def get_feature_distribution():
    directory = '/home/priyank/Desktop/7thSem/ML_Project/data/mentionsWithSentenceNums/'
    # directory = '/home/priyank/Desktop/7thSem/ML_Project/data/justForTest/'
    print "Loading data"
    x,y = load_dataset(directory)
    f_true = [{},{},{},{},{},{},{}]
    f_false = [{},{},{},{},{},{},{}]
    print "Getting Distributions"
    for X,Y in zip(x,y):
        if Y == 1:
            for i in range(len(X)):
                if X[i] == True:
                    X[i] = 1
                elif X[i] == False:
                    X[i] = 0
                try:
                    f_true[i][X[i]] += 1
                except:
                    f_true[i][X[i]] = 1
        else:
            for i in range(len(X)):
                if X[i] == True:
                    X[i] = 1
                elif X[i] == False:
                    X[i] = 0
                try:
                    f_false[i][X[i]] += 1
                except:
                    f_false[i][X[i]] = 1

    pkl.dump(f_true,open('feature_distributions_true.pkl','wb'))
    pkl.dump(f_false,open('feature_distributions_false.pkl','wb'))

    print f_true


names = [#"Nearest Neighbors", 
        "Linear SVM", "RBF SVM", "Decision Tree",
         "Random Forest", "AdaBoost", "Naive Bayes", "LogisticRegression"]# "Linear Discriminant Analysis",
         # "Quadratic Discriminant Analysis"]


classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    GaussianNB(),
    # LinearDiscriminantAnalysis(),
    # QuadraticDiscriminantAnalysis()
    LogisticRegression()
    ]

def main_multiple_classifiers():
    pickle_directory = '/home/priyank/Desktop/7thSem/ML_Project/codes_new/pickles_new/'
    directory = '/home/priyank/Desktop/7thSem/ML_Project/data/mentionsWithMayBeSubject/'
    try:
        raise Exception('Reload dataset')
        x_train = pkl.load(open(pickle_directory+'x_train.pkl','r'))
        x_test = pkl.load(open(pickle_directory+'x_test.pkl','r'))
        y_train = pkl.load(open(pickle_directory+'y_train.pkl','r'))
        y_test = pkl.load(open(pickle_directory+'y_test.pkl','r'))
    except:
        print 'Reloading Dataset'
        x_train,y_train,x_test,y_test,rule_based_wrong_count,rule_based_correct_count = load_dataset(directory,pickle_directory)
        # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.4, random_state=42)
        pkl.dump(x_train, open(pickle_directory+'x_train.pkl','wb'))
        pkl.dump(x_test, open(pickle_directory+'x_test.pkl','wb'))
        pkl.dump(y_train, open(pickle_directory+'y_train.pkl','wb'))
        pkl.dump(y_test, open(pickle_directory+'y_test.pkl','wb'))




    for name, clf in zip(names, classifiers):
        print(name)
        coll = []
        try:
            raise Exception('Retrain, Bitch!')
            # with open(pickle_directory + name + '.pkl', 'rb') as f1:
            #     clf = pkl.load(f1)
        except:
            clf.fit(x_train, y_train)
            with open(pickle_directory + name + '.pkl', 'wb') as f1:
                pkl.dump(clf, f1)

        coll = clf.predict(x_test)
        #print(coll[10:50], y_test[10:50])
        # for vals in X_test:
        #     z = clf.predict([vals])

        #     coll.append(z[0])
        score = evaluate(y_test, coll)
        print(metrics.classification_report(y_test, coll))
        #print(str(score))
        # f = open(name + '.txt', 'w')
        # f.write(str(score))

if __name__ == '__main__':
    main_multiple_classifiers()
    # get_feature_distribution()
    # main_for_simple_testing()