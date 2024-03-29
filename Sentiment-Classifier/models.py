# models.py

from sentiment_data import *
from utils import *
from collections import Counter
import numpy as np 
from nltk.corpus import stopwords
import math

class FeatureExtractor(object):
    """
    Feature extraction base type. Takes a sentence and returns an indexed list of features.
    """

    def get_indexer(self):
        raise Exception("Don't call me, call my subclasses")

    def extract_features(self, ex_words: List[str], add_to_indexer: bool=False) -> Counter:
        """
        Extract features from a sentence represented as a list of words. Includes a flag add_to_indexer to
        :param sentence: words in the example to featurize
        :param add_to_indexer: True if we should grow the dimensionality of the featurizer if new features are encountered.
        At test time, any unseen features should be discarded, but at train time, we probably want to keep growing it.
        :return: A feature vector. We suggest using a Counter[int], which can encode a sparse feature vector (only
        a few indices have nonzero value) in essentially the same way as a map. However, you can use whatever data
        structure you prefer, since this does not interact with the framework code.
        """
        raise Exception("Don't call me, call my subclasses")


class UnigramFeatureExtractor(FeatureExtractor):
    """
    Extracts unigram bag-of-words features from a sentence. It's up to you to decide how you want to handle counts
    and any additional preprocessing you want to do.
    """

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def get_indexer(self):
        return self.indexer

    def extract_features(self, ex_words: List[str], add_to_indexer: bool) -> List[int]:
        str_features = np.zeros(self.indexer.__len__())
        for ele in ex_words:
            if self.indexer.contains(ele.lower()):
                str_features[self.indexer.index_of(ele.lower())] += 1
        return str_features

class BigramFeatureExtractor(FeatureExtractor):
    """
    Bigram feature extractor analogous to the unigram one.
    """
    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def get_indexer(self):
        return self.indexer

    def extract_features(self, ex_words: List[str], add_to_indexer: bool) -> List[int]:
        str_features = np.zeros(self.indexer.__len__(),dtype=int)
        for i in range(0, len(ex_words)-1):
            bigram = ex_words[i] + ' ' + ex_words[i + 1]
            if self.indexer.contains(bigram.lower()):
                index = self.indexer.index_of(bigram.lower())
                str_features[index] += 1
        return str_features

class BetterFeatureExtractor(FeatureExtractor):
    """
    Better feature extractor...try whatever you can think of!
    """
    def __init__(self, indexer: Indexer):
        raise Exception("Must be implemented")


class SentimentClassifier(object):
    """
    Sentiment classifier base type
    """

    def predict(self, ex_words: List[str]) -> int:
        """
        :param sentence: words (List[str]) in the sentence to classify
        :return: Either 0 for negative class or 1 for positive class
        """
        raise Exception("Don't call me, call my subclasses")


class TrivialSentimentClassifier(SentimentClassifier):
    """
    Sentiment classifier that always predicts the positive class.
    """

    def predict(self, sentence: List[str]) -> int:
        return 1


class PerceptronClassifier(SentimentClassifier):
    """
    Implement this class -- you should at least have init() and implement the predict method from the SentimentClassifier
    superclass. Hint: you'll probably need this class to wrap both the weight vector and featurizer -- feel free to
    modify the constructor to pass these in.
    """
    # def __init__(self, ex_words: List[str], feat_extractor):
    #     self.feat_extractor = feat_extractor
    #     # training perceptron
    #     n = len(ex_words)
    #     m = self.feat_extractor.extract_features(ex_words, False)
    #     weight_vector = np.zeros([m])
    #     Epoch = 10
    #     for i in range(Epoch):
    #         # store correct classification
    #         acc = np.zeros([n])
    #         for j in range(n):
    #             feat 
    def __init__(self):
        raise Exception("Must be implemented")

class LogisticRegressionClassifier(SentimentClassifier):
    """
    Implement this class -- you should at least have init() and implement the predict method from the SentimentClassifier
    superclass. Hint: you'll probably need this class to wrap both the weight vector and featurizer -- feel free to
    modify the constructor to pass these in.
    """

    def __init__(self, weights: np.ndarray, feat_extractor: FeatureExtractor):
        self.weights = weights
        self.feat_extractor = feat_extractor

    def predict(self, ex_words: List[str]) -> int:
        str_features = self.feat_extractor.extract_features(ex_words, False)
        expo = math.exp(np.dot(self.weights, str_features))
        possibility = expo / (1 + expo)
        if possibility > 0.5:
            return 1
        return 0


def train_perceptron(train_exs: List[SentimentExample], feat_extractor: FeatureExtractor) -> PerceptronClassifier:
    """
    Train a classifier with the perceptron.
    :param train_exs: training set, List of SentimentExample objects
    :param feat_extractor: feature extractor to use
    :return: trained PerceptronClassifier model
    """
    raise Exception("Must be implemented")


def train_logistic_regression(train_exs: List[SentimentExample], feat_extractor: FeatureExtractor) -> LogisticRegressionClassifier:
    """
    Train a logistic regression model.
    :param train_exs: training set, List of SentimentExample objects
    :param feat_extractor: feature extractor to use
    :return: trained LogisticRegressionClassifier model
    """
    indexer = feat_extractor.get_indexer()
    weights = np.transpose(np.zeros(indexer.__len__(), dtype=int))
    learning_rate = 0.0001
    Epoch = 10
    for i in range(Epoch):
        for ex in train_exs:
            str_features = feat_extractor.extract_features(ex.words, False)
            expo = math.exp(np.dot(weights, str_features))
            possibility = expo / (1 + expo)
            w_gradient = np.dot(ex.label - possibility, str_features)
            weights = np.add(weights, np.dot(learning_rate, w_gradient))
    return LogisticRegressionClassifier(weights, feat_extractor)
    # 0.01 learning rate per 45 Epochs for 0.77% in 14 seconds: unigrams
    # _ learning rate per _ Epochs for in _ seconds

def train_model(args, train_exs: List[SentimentExample], dev_exs: List[SentimentExample]) -> SentimentClassifier:
    """
    Main entry point for your modifications. Trains and returns one of several models depending on the args
    passed in from the main method. You may modify this function, but probably will not need to.
    :param args: args bundle from sentiment_classifier.py
    :param train_exs: training set, List of SentimentExample objects
    :param dev_exs: dev set, List of SentimentExample objects. You can use this for validation throughout the training
    process, but you should *not* directly train on this data.
    :return: trained SentimentClassifier model, of whichever type is specified
    """
    indexer = Indexer()
    stop_words = set(stopwords.words('english'))
    punkt = (',','.',', ','...','?','\'','\'\'','!',';',':')
    # Initialize feature extractor
    if args.model == "TRIVIAL":
        feat_extractor = None
    elif args.feats == "UNIGRAM":
        # Vocabulary
        for ex in train_exs:
            for word in ex.words:
                if word.lower() not in stop_words and word.lower() not in punkt:
                    indexer.add_and_get_index(word.lower())
        feat_extractor = UnigramFeatureExtractor(indexer)
    elif args.feats == "BIGRAM":
        # Add additional preprocessing code here
        for ex in train_exs:
            for i in range(0, len(ex.words) - 1):
                if stop_words.__contains__(ex.words[i]) and stop_words.__contains__(ex.words[i+1]) or (
                        punkt.__contains__(ex.words[i]) or punkt.__contains__(ex.words[i+1])):
                    continue
                bigram = ex.words[i] + ' ' + ex.words[i + 1]
                indexer.add_and_get_index(bigram.lower())
        feat_extractor = BigramFeatureExtractor(indexer)
    elif args.feats == "BETTER":
        # Add additional preprocessing code here
        feat_extractor = BetterFeatureExtractor(Indexer())
    else:
        raise Exception("Pass in UNIGRAM, BIGRAM, or BETTER to run the appropriate system")

    # Train the model
    if args.model == "TRIVIAL":
        model = TrivialSentimentClassifier()
    elif args.model == "PERCEPTRON":
        model = train_perceptron(train_exs, feat_extractor)
    elif args.model == "LR":
        model = train_logistic_regression(train_exs, feat_extractor)
    else:
        raise Exception("Pass in TRIVIAL, PERCEPTRON, or LR to run the appropriate system")
    return model