# MoralChoiceMachine

required packages: tensorflow, fensorflow_hub, scipy, numpy, logging

### Included Files   
* MoralChoiceMachine  --- core algorithms 
* data.py             --- input data for different experiments that are reported in the paper
* experiments.py      --- calls of basic experiments
* util.py             --- side functions

### Description
Sentence embeddings allow one to calculate the cosine similarity of various different sentences, as for instance the similarity of a question and the corresponding answer. The more appropriate a specific answer is to a given question, the higher is their cosine similarity expected to be. When considering two opposite answers, it is therefore possible to determine a bias value.

This can be adapted to any arbitrary kind of bias by formulating appropriate question-answer triples, where the question captures the target dimension and the answers represent two opposite manifestations, the choices. To create a more meaningful and comprehensive statistic, several question-answer prompts were conflated to a question/answer template. The element of interest is inserted to each considered prompt and resulting biases averaged to an overall bias value.
Specifically, we considered two different biases: gender and moral. 
