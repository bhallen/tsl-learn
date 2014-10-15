#!/usr/bin/env python

import csv
import itertools
import re
import math
from collections import defaultdict

## NEED TO DO:
## - implement MI function, verify that U(w)-M_1(w) = plog of bigram model

## TO-DO (things not in G&R):
## - add backward probabilities
## - add final bigram probability (right edge symbol | last segment)

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
        ungrammatical
        """
        self.read_training_file(training)
        self.get_sigma(sigma)
        self.max_k = max_k
        # self.build_tiers()


    def find_unigrams(self, lexicon, smoothing=True):
        uni_dict = defaultdict(int)
        total = 0.0
        for form in lexicon:
            for symbol in form:
                uni_dict[symbol] += 1.0
                total += 1.0
        if smoothing:
            for symbol in self.sigma:
                uni_dict[symbol] += 0.5
                total += 0.5
        self.unigram_sum = total
        return {symbol: uni_dict[symbol]/total for symbol in uni_dict}

    def find_bigrams(self, lexicon, smoothing=True):
        bi_dict = defaultdict(int)
        total = 0.0
        for form in lexicon:
            bigrams = self.get_ngrams(form, 2)
            for bg in bigrams:
                bi_dict[bg] += 1.0
                total += 1.0
        if smoothing:
            for bg in itertools.product(self.sigma+['#'], repeat=2): # remove '##'?
                bi_dict[bg] += 0.5
                total += 0.5
        self.bigram_sum = total
        return {symbol: bi_dict[symbol]/total for symbol in bi_dict}

    def create_tier_lexicon(self, tier):
        return [[symbol for symbol in form if symbol in tier] for form in self.lexicon]

    def unigram_plog(self, lexicon, unigrams):
        plog = 0
        for form in lexicon:
            for symbol in form:
                plog += math.log(unigrams[symbol])
        return -(plog)

    def bigram_plog(self, lexicon, bigrams, unigrams):
        plog = 0
        for form in lexicon:
            for bg in [tuple(form[i:i+2]) for i in range(1, len(form)-1)]:
                plog += math.log((bigrams[bg]*self.bigram_sum) / (unigrams[bg[0]]*self.unigram_sum))
        return -(plog)


####


    def learn(self):
        """
        Original learning algorithm; uses brute-force search of all bigrams on all possible tiers to create a categorical grammar.
        """
        self.grammatical = {}
        self.ungrammatical = {}
        for tier in self.tiers:
            tier_grammatical = []
            possible_ngrams = set(itertools.chain.from_iterable(itertools.product(tier, repeat=r) for r in range(1,self.max_k+1)))
            for form in self.lexicon:
                on_tier = [s for s in form if s in tier]
                # print(tier)
                # print(form)
                # print(on_tier)
                # print() 
                tier_grammatical += self.get_uni_to_ngrams(on_tier, self.max_k) # function was refactored; needs checking
            grammatical_set = set(tier_grammatical)
            ungrammatical_set = possible_ngrams - grammatical_set
            self.grammatical[tuple(tier)] = grammatical_set
            self.ungrammatical[tuple(tier)] = ungrammatical_set


    def read_training_file(self, training_file):
        with open(training_file) as tf:
            lines = csv.reader(tf, delimiter='\t')
            self.lexicon = [['#']+line[0].strip().split(' ')+['#'] for line in lines]


    def get_sigma(self, sigma_file):
        if sigma_file == None:
            # infer from self.training
            merged_data = list(itertools.chain.from_iterable(self.lexicon))
            self.sigma = list(set(merged_data))
        else:
            # TO-DO: read file
            pass


    def get_ngrams(self, sequence, n):
        return zip(*[sequence[i:] for i in range(n)])

    def get_uni_to_ngrams(self, sequence, max_k):
        return list(itertools.chain.from_iterable([get_ngrams(sequence, n) for n in range(max_k+1)]))


if __name__ == '__main__':
    # TESTING
    g = Grammar('shona/training.txt')
    # print(g.lexicon)
    # print(g.sigma)
    # print(g.tiers)

    # print(g.create_tier_lexicon(['a','e','i','u','e']))

    ugs = g.find_unigrams(g.lexicon)
    print(g.unigram_plog(g.lexicon, ugs))

    tugs = g.find_unigrams(g.create_tier_lexicon(['a','e','i','u','e']))
    print(g.unigram_plog(g.create_tier_lexicon(['a','e','i','u','e']), tugs))

    bgs = g.find_bigrams(g.lexicon)
    print(g.bigram_plog(g.lexicon, bgs, ugs))

    tbgs = g.find_bigrams(g.create_tier_lexicon(['a','e','i','u','e']))
    print(g.bigram_plog(g.create_tier_lexicon(['a','e','i','u','e']), tbgs, tugs))

    # print(g.find_bigrams(g.create_tier_lexicon(['a','e','i','u','e'])))



    # g.learn()
    # print(g.grammatical)
