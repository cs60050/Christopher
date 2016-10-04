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
	* Distances between the two mentions in terms of the no of sentences and the no of mentions occuring between them.
	* String matching features indicating if the mentions have matching head words,match partially, or match exactly.
	* String matching features indicating if the mentions words,match partially, or match exactly.


### Tools
* For word vectors, we have used a pretrained word2vec model on the Google News corpus.
* For dependency parsing, we have used the Stanford Core NLP module.

### Network architecture
To be added

### Datasets
To be added

### Accuracy
To be added
