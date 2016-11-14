import cPickle as pkl
import os

def create(fname):
	a = pkl.load(open("x_train/"+fname,"rb"))
	b = pkl.load(open("y_train/"+fname[:-1],"r"))

	i = 0
	j = 0

	trueT = 0
	for i in b:
		trueT += i[1]

	Xtrain = []
	Xtest = []

	Ytrain = []
	Ytest = []

	count = 0

	print trueT

	for i in range(len(a)):
		if b[i][1] == 1:
			if count < (0.7*trueT): 
				Xtrain.append(a[i])
				Ytrain.append(b[i])
			else:
				Xtest.append(a[i])
				Ytest.append(b[i])
			while b[j][1] == 1:
				j = j+1
				if j>=len(b):
					break
			if j>=len(b):
					break
			if count < (0.7*trueT):
				# print len(a)
				#print j
				#print len(b) 
				Xtrain.append(a[j])
				Ytrain.append(b[j])
			else:
				Xtest.append(a[j])
				Ytest.append(b[j])
	
			count = count + 1
			if count == trueT:
				break


	pkl.dump(Xtrain, open("x_train_"+fname,"wb"), -1)
	pkl.dump(Xtest, open("x_test_"+fname,"wb"), -1)
	pkl.dump(Ytrain, open("y_train_"+fname,"wb"), -1)
	pkl.dump(Ytest, open("y_test_"+fname,"wb"), -1)

files = os.listdir("./x_train")
print files
for f in files:
	print f[-3:]
	if f[-3:] == ".pb":
		print f
		create(f)
