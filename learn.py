#!/usr/bin/env python

import itertools
import re

class Grammar(dict):
    """
    """
    def __init__(self, training, sigma=None, max_k=2):
        """
        Attributes:
        lexicon
        sigma
        max_k
        tiers
        grammatical
        """
        self.read_training_file(training)
        self.get_sigma(sigma)
        self.max_k = max_k
        self.build_tiers()


    def learn(self):
        """
        """
        self.grammatical = {}
        for tier in self.tiers:
            tier_grammatical = []
            for form in self.lexicon:
                on_tier = [s for s in form if s in tier]
                # print(tier)
                # print(form)
                # print(on_tier)
                # print() 
                tier_grammatical += self.get_ngrams(on_tier, self.max_k)
            self.grammatical[tuple(tier)] = set(tier_grammatical)


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
            # TO-DO: read file
            pass


    def build_tiers(self):
        """All possible tiers
        """
        self.tiers = list(itertools.chain.from_iterable(itertools.combinations(self.sigma, r) for r in range(1,len(self.sigma)+1)))


    def get_ngrams(self, sequence, max_k):
        return list(itertools.chain.from_iterable([zip(*[sequence[i:] for i in range(n)]) for n in range(max_k+1)]))


if __name__ == '__main__':
    # TESTING
    g = Grammar('training_unbounded_harm_restricted.txt')
    # print(g.lexicon)
    # print(g.sigma)
    # print(g.tiers)

    g.learn()
    # print(g.grammatical)
    for t in g.grammatical:
        print(t)
        print(g.grammatical[t])
        print()