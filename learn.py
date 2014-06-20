#!/usr/bin/env python

import itertools
import re

class Grammar(dict):
    """
    """
    def __init__(self, training, sigma=None, max_k=2):
        self.read_training_file(training)
        self.get_sigma(sigma)
        self.max_k = max_k

        self.tiers = []


    def learn():
        """
        """
        # 
        pass


    def read_training_file(self, training_file):
        with open(training_file) as tf:
            lines = tf.read().rstrip().replace('\r','\n').replace('\n\n','\n').split('\n')
            self.lexicon = [line.split(' ') for line in lines]


    def get_sigma(self, sigma_file):
        if sigma_file == None:
            # infer from self.training
            merged_data = list(itertools.chain.from_iterable(self.lexicon))
            self.sigma = list(set(merged_data))
        else:
            # read file
            pass

    def ngrams(self, sequence, max_k):
        return list(itertools.chain.from_iterable([zip(*[sequence[i:] for i in range(n)]) for n in max_k]))


if __name__ == '__main__':
    # TESTING
    g = Grammar('training_unbounded_harm_restricted.txt')
    print(g.lexicon)
    print(g.sigma)