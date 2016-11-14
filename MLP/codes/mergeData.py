import cPickle as pkl
import os

files = os.listdir("./")
x_train = pkl.load(open("x_train.pb",'rb'))
x_test = pkl.load(open("x_test.pb",'rb'))
y_train = pkl.load(open("y_train.pb",'rb'))
y_test = pkl.load(open("y_test.pb",'rb'))

print files
for f in files:
	if "msnbc" in f:
		print f
		a = pkl.load(open(f,"rb"))
		if "x_train" in f:
			x_train += a
		elif "x_test" in f:
			x_test += a
		elif "y_train" in f:
			y_train += a
		elif "y_test" in f:
			y_test += a

		del a

print len(x_train)
print len(x_test)
print len(y_train)
print len(y_test)

pkl.dump(x_train, open("x_train.pb",'wb'), -1)
pkl.dump(x_test, open("x_test.pb",'wb'), -1)
pkl.dump(y_train, open("y_train.pb",'wb'), -1)
pkl.dump(y_test, open("y_test.pb",'wb'), -1)

del x_train
del x_test
del y_train
del y_test
