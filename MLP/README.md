# Co-Reference Resolution using Neural Networks
#### Contributers: Barnopriyo Barua & Vadde Santosha Pradeep Chandra
This is an implementation of the co-reference resultion task using Multi Layer Perceptrons. This method is based on the [paper](https://cs224d.stanford.edu/reports/ClarkKevin.pdf) by Clark Kelvin. 

### Tools
* For word vectors, we have used a pretrained word2vec model on the Google News corpus. Each word vector has a dimension of 300.
* For dependency parsing, we have used the Stanford Core NLP module.
* For POS tagging, we have used NLTK's Maximum Entropy POS Tagger.

### Features
1. Mention Features (1201-d)
	* Word vectors for the first, last, and head words of the mention. (900-d)
	* The average of all word vectors in the mention. (300-d)
	* The dependency relation between the head word of the mention and its parent. (1-d)
2. Context Features (300-d)
	* Average of all word vectors to the left and right of the mention in a window of size 5. (300-d)
3. Mention pair Features (4-d)
	* Distances between the two mentions in terms of the number of sentences and the number of mentions occurring between them. (2-d)
	* String matching feature indicating if the head words of the mention match partially or exactly. (1-d)
	* String matching feature indicating if the mentions word match partially or exactly. (1-d)

Each input corresponds to a pair of mentions. The size of this input vector was 3006.

|  M1 (1201)  |  M2 (1201)  |  C1 (300)  |  C2 (300)  |  P (4)  |


### Intermediate Data files
Precomputed data files required during the feature extarction process can be found [here](https://drive.google.com/drive/folders/0BwwGVSvxwm9QYnJEbTRpTXN0SFk?usp=sharing).

### Network architecture
We use a simple neural network which takes a pair of mentions as input and predicts if both point to the same entity or not. There are no connections between the hidden units of two different time stamps. Our network architecture consists to 2 hidden layers. Each hidden layer contains 1503 hidden units and is followed by a ReLU layer.

### Train and Test Datasets
The CoNLL 2012 trial corpus is divided into 10 different parts, the biggest of them being the msnbc_0004 which consists of 1253 mentions. This results in a total of around 7,50,000 mention pairs in that particular part out of which only a little over 1% are true, i.e., coreferent. This is giving rise to a huge dataset, which combined with our 3006 vector for each pair, is very difficult to process and load. So, instead of using all the pairs for training and testing, we have decided to consider all the true pairs in our dataset along with an equal number of false pairs. This reduces the size of the dataset by a huge margin.
From the mention pairs obtained using the procedure decribed above, we created 5 datasets by grouping them, which have been used to get the observations as can been seen from the report.

### Accuracy
We run 3 different experiments with different combinations of these datasets and note the accuracies. We achieved good accuracies in these experiments. In addition to this, we also observed how the accuracy converged after various epochs of training the network. We also observed the change in accuracy with increasing epochs and noted the convergence point. All the results are properly mentioned and documented in the report. 
