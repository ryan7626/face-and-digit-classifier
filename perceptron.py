# perceptron.py
# -------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Perceptron implementation
import util
PRINT = True

class PerceptronClassifier:
    """
    Perceptron classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "perceptron"
        self.max_iterations = max_iterations
        self.weights = {}
        for label in legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def setWeights(self, weights):
        assert len(weights) == len(self.legalLabels);
        self.weights = weights;

    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        """
        The training loop for the perceptron passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        See the project description for details.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        (and thus represents a vector a values).
        """
        self.features = trainingData[0].keys() # could be useful later

        for iteration in range(self.max_iterations):
            print ("Starting iteration ", iteration, "...")
            for i in range(len(trainingData)):
                real, pred = trainingLabels[i], self.classify([trainingData[i]])[0]
                if real != pred:
                    self.weights[real] += trainingData[i]
                    self.weights[pred] -= trainingData[i]

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


    def findHighWeightFeatures(self, label):
    #Returns a list of the 100 features with the greatest weight for some label

        featuresWeights = []

        # Sort the features by weight in descending order
        sortedFeatures = sorted(self.weights[label].items(), key=lambda x: x[1], reverse=True)

        # Take the top 100 features
        topFeatures = sortedFeatures[:100]

        # Append the feature names to the list
        featuresWeights = [feature for feature, weight in topFeatures]
        return featuresWeights
    
    import numpy as np

def perceptron_loss(weights, bias, X, y):
    n_samples = X.shape[0]
    predictions = np.dot(X, weights) + bias
    predictions = np.where(predictions >= 0, 1, -1)  # Apply the step function
    
    misclassified = np.where(predictions != y, 1, 0)  # Identify misclassified samples
    loss = 0.5 * np.sum(np.square(misclassified * (y - predictions)))  # Compute the loss
    
    return loss