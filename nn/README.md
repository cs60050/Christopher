# Co-Reference Resolution using Neural Networks
#### Contributers: Barnopriyo Barua & Vadde Santosha Pradeep Chandra
This is an implementation of the co-reference resultion task using Multi Layer Perceptrons. This method is based on the [paper](https://cs224d.stanford.edu/reports/ClarkKevin.pdf) by Clark Kelvin. 

### Features
1. Mention Features
	* Word vectors for the first, last, and head words of the mention.
	* The average of all word vectors in the mention.
	* The dependency relation between the head word of the mention and its parent.
2. Context Features
	* Average of all word vectors to the left and right of the mention in a window of size 5.
3. Mention pair Features
	* Distances between the two mentions in terms of the number of sentences and the number of mentions occuring between them.
	* String matching feature indicating if the head words of the mention match partially or exactly.
	* String matching feature indicating if the mentions word match partially or exactly.

### Intermediate Data files
Precomputed data files required during the feature extarction process can be found [here](https://drive.google.com/drive/folders/0BwwGVSvxwm9QYnJEbTRpTXN0SFk?usp=sharing).

### Tools
* For word vectors, we have used a pretrained word2vec model on the Google News corpus. Each word vector has a dimension of 300.
* For dependency parsing, we have used the Stanford Core NLP module.

### Network architecture
To be added

### Train and Test Datasets
To be added

### Accuracy
To be added
