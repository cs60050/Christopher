import cPickle as pkl

a = pkl.load(open("msnbc_0004.p",'rb'))

print "Load done"

f = open("msnbc_0004.pb",'wb')
pkl.dump(a,f,-1)
