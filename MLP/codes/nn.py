import tensorflow as tf
import pickle
import numpy as np
import time;



def ml(corpus,trueInd,merged="",vector_size= 3006,nh1=1503,nh2=1503):
    ni = vector_size
    print("*******************************")
    print(merged + " " + corpus)
    print("*******************************")
    x_train = open(merged+"all_corpus/x_train"+corpus+".pb","rb")
    print "xTrain loaded"
    x_train = pickle.load(x_train)
    total_words = len(x_train)
    # x_train_arr = np.array(x_train)
    x_test = open(merged+"all_corpus/x_test"+corpus+".pb","rb")
    print "xTest loaded"
    x_test = pickle.load(x_test)
    # x_test_arr = np.array(x_test)

    y_train = open("all_corpus/y_train"+corpus+".pb","rb")
    print "yTrain loaded"
    y_train = pickle.load(y_train)
    y_train = [x[1] for x in y_train]
    # y_train_list = y_train
    tt = sum(y_train)
    for i in range(len(x_train)):
        temp = [0,0]
        temp[y_train[i]] = 1
        y_train[i] = temp
    # print y_train
    
    # return
    y_test = open("all_corpus/y_test"+corpus+".pb","rb")
    print "yTest loaded"
    y_test = pickle.load(y_test)
    y_test = [x[1] for x in y_test]

    for i in range(len(x_test)):
        temp = [0,0]
        temp[y_test[i]] = 1
        y_test[i] = temp

    # y_train_arr = np.array(y_train)

    # Parameters
    learning_rate = 0.001
    training_epochs = 200
    batch_size = 100
    display_step = 1

    localtime = time.asctime( time.localtime(time.time()) )
    file = open("accuracies_All_corpus_data" + corpus,"a")
    file.write("time = " + localtime + "\nlearning_rate = 0.001\ntraining_epochs = 100\nbatch_size = 100\ntrueInd = " + str(trueInd) + "\n\n")
    file.write('\nTrail : all data 70 %\nTest : all data 30%\n\n')
    # Network Parameters
    n_hidden_1 = nh1 # 1st layer number of features
    n_hidden_2 = nh2 # 2nd layer number of   features
    n_input = ni # MNIST data input (img shape: 28*28)
    n_classes = 2 # MNIST total classes (0-9 digits)

    # tf Graph input
    x = tf.placeholder("float", [None, ni])
    y = tf.placeholder("float", [None, 2])

    # print type(y_train[0])

    def getBatch(i,batch_size):
        start = i*batch_size
        return np.array(x_train[start:start+batch_size]), np.array(y_train[start:start+batch_size])


    # Store layers weight & bias
    weights = {
        'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_classes]))
    }
    # Create model
    def multilayer_perceptron(x, weights=weights, biases=biases):
        # Hidden layer with RELU activation
        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
        layer_1 = tf.nn.relu(layer_1)
        # Hidden layer with RELU activation
        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        layer_2 = tf.nn.relu(layer_2)
        # Output layer with linear activation
        out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
        return out_layer



    # Construct model
    pred = multilayer_perceptron(x, weights, biases)

    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    # Initializing the variables
    init = tf.initialize_all_variables()


    # Launch the graph
    with tf.Session() as sess:
        sess.run(init)

        # Training cycle
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(total_words/batch_size)
            # Loop over all batches
            for i in range(total_batch):
                batch_x, batch_y = getBatch(i,batch_size)
                # print(batch_y.shape)
                # Run optimization op (backprop) and cost op (to get loss value)
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
                # Compute average loss
                avg_cost += c / total_batch
            # Display logs per epoch step
            if epoch % display_step == 0:
                print "Epoch:", '%04d' % (epoch+1), "cost=", \
                    "{:.9f}".format(avg_cost)
                for i in range(len(x_test)):
                    x_test[i] = np.array(x_test[i],dtype="float32")
                x_test_arr = np.array(x_test,dtype="float32")
                # print len(x_test)
                # print len(x_test_arr)
                predic = multilayer_perceptron(x_test_arr).eval()

                res = []


                for p in predic:
                    if p[trueInd]<p[1-trueInd]:
                        res.append(0)
                    else:
                        res.append(1)

                # print "res ", len(predic)
                # print "y ", len(y_test)

                # file = open(merged+"y_predicted"+corpus+".pb","wb")
                # pickle.dump(res,file)

                tp = 0
                fp = 0
                tn = 0
                fn = 0

                # print "&&&&&&&&&&&&&&&&&&&&"
                # print y_test
                for i in range(len(y_test)):
                    if y_test[i][1] == 1:
                        if res[i] == 1:
                            tp = tp + 1
                        else:
                            fn = fn + 1

                    else:
                        if res[i] == 1:
                            fp = fp + 1
                        else:
                            tn = tn + 1

                precision = float(tp)/float(tp+fp)
                recall = float(tp)/float(tp+fn)
                if precision != 0 and recall != 0 :
                    fscore = (2*(precision*recall))/(precision+recall)
                else :
                    fscore = 0
                file = open("accuracies_All_corpus_data" + corpus,"a")
                file.write("Epoch " + str(epoch) + "\n")
                #file.write("CORPUS = " + corpus + "\n")
                #file.write("TRAIN SET" + "\n")
                file.write("\tTrue Positives = " + str(tp) + "\n")
                file.write("\tTrue Negatives = " + str(tn) + "\n")
                #file.write("TEST SET" + "\n")
                file.write("\tFalse positives = " + str(fp) + "\n")
                #y_temp = []
                #for a in y_test:
                #    y_temp.append(a[1])
                file.write("\tFalse negatives = " + str(fn) + "\n")
                file.write("ACCURACIES" + "\n")
                file.write("\tPrecision = " + str(precision) + "\n")
                file.write("\tRecall = " + str(recall) + "\n")
                file.write("\tfscore = " + str(fscore))
                # for i in range(len(res)):
                #     print res[i], " ", y_temp[i]
                # print y_test
                file.write("\n\n")

        print "Optimization Finished!"

        for i in range(len(x_test)):
            x_test[i] = np.array(x_test[i],dtype="float32")
        x_test_arr = np.array(x_test,dtype="float32")
        # print len(x_test)
        # print len(x_test_arr)
        predic = multilayer_perceptron(x_test_arr).eval()

        res = []


        for p in predic:
            if p[trueInd]<p[1-trueInd]:
                res.append(0)
            else:
                res.append(1)

        # print "res ", len(predic)
        # print "y ", len(y_test)

        file = open(merged+"y_predicted"+corpus+".pb","wb")
        pickle.dump(res,file)

        tp = 0
        fp = 0
        tn = 0
        fn = 0

        # print "&&&&&&&&&&&&&&&&&&&&"
        # print y_test
        for i in range(len(y_test)):
            if y_test[i][1] == 1:
                if res[i] == 1:
                    tp = tp + 1
                else:
                    fn = fn + 1

            else:
                if res[i] == 1:
                    fp = fp + 1
                else:
                    tn = tn + 1

        precision = float(tp)/float(tp+fp)
        recall = float(tp)/float(tp+fn)
        if precision != 0 and recall != 0 :
            fscore = (2*(precision*recall))/(precision+recall)
        else :
            fscore = 0
        file = open("accuracies_All_corpus_data" + corpus,"a")
        file.write("*****************\nFINAL\n")
        file.write("CORPUS = all - msnbc" + corpus + "\n")
        file.write("TRAIN SET" + "\n")
        file.write("\tTotal Tokens = " + str(len(x_train)) + "\n")
        file.write("\tTrue Tokens = " + str(tt) + "\n")
        file.write("TEST SET" + "\n")
        file.write("\tTotal Tokens = " + str(len(x_test)) + "\n")
        y_temp = []
        for a in y_test:
            y_temp.append(a[1])
        file.write("\tTrue Tokens = " + str(sum(y_temp)) + "\n")
        file.write("\tTrue Positives = " + str(tp) + "\n")
        file.write("\tTrue Negatives = " + str(tn) + "\n")
        #file.write("TEST SET" + "\n")
        file.write("\tFalse positives = " + str(fp) + "\n")
        #y_temp = []
        #for a in y_test:
        #    y_temp.append(a[1])
        file.write("\tFalse negatives = " + str(fn) + "\n")
        file.write("ACCURACIES" + "\n")
        file.write("\tPrecision = " + str(precision) + "\n")
        file.write("\tRecall = " + str(recall) + "\n")
        file.write("\tfscore = " + str(fscore))
        # for i in range(len(res)):
        #     print res[i], " ", y_temp[i]
        # print y_test
        file.write("\n\n")

# ml("NCBI","merged_",500,500,1000)
# ml("NCBI")
# ml("TITLES")
# ml("ABSTRACT")
# ml("SENTENCES")
# ml("chtb_0192",3006)
ml("",0)
#ml("",1)
        
        
