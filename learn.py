#!/usr/bin/env python

import itertools
import re
from collections import defaultdict

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
        self.build_tiers()


    def learn(self):
        """
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
                tier_grammatical += self.get_ngrams(on_tier, self.max_k)
            grammatical_set = set(tier_grammatical)
            ungrammatical_set = possible_ngrams - grammatical_set
            self.grammatical[tuple(tier)] = grammatical_set
            self.ungrammatical[tuple(tier)] = ungrammatical_set


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
        Each tier is a tuple in alphabetical order
        """
        self.tiers = []
        for size in range(1,len(self.sigma)+1):
            for combo in itertools.combinations(self.sigma, size):
                self.tiers.append(tuple(sorted(list(combo))))


    def distill_grammar(self):
        grammar = defaultdict(list)
        for kfactor in itertools.permutations(self.sigma, 2): # could this consider instead only bigrams prohibited on the segment tier?
            relevant_tier = self.traverse_lattice(kfactor)
            if relevant_tier != None:
                grammar[relevant_tier].append(kfactor)
        return grammar


    def traverse_lattice(self, kfactor):
        """
        """
        initial_tier = set(kfactor)
        not_in_kfactor = set(self.sigma) - initial_tier

        initial_tier_tuple = tuple(sorted(kfactor))
        if kfactor in self.ungrammatical[initial_tier_tuple]:
            return initial_tier_tuple

        result = initial_tier.copy()
        for char in not_in_kfactor:
            combined_tier = initial_tier.union(set([char]))
            combined_tier_tuple = tuple(sorted(list(combined_tier)))
            if kfactor in self.ungrammatical[combined_tier_tuple]:
                result.add(char)

        if result == initial_tier:
            full_tier = tuple(sorted(self.sigma))
            if kfactor in self.ungrammatical[full_tier]:
                return full_tier
            else:
                return None
        else:
            return tuple(sorted(list(result)))


    def tiers_equal(tier1, tier2):
        return set(tier1) == set(tier2)
        

    def get_ngrams(self, sequence, max_k):
        return list(itertools.chain.from_iterable([zip(*[sequence[i:] for i in range(n)]) for n in range(max_k+1)]))


if __name__ == '__main__':
    g = Grammar('cvlrb6_blocking.txt')

    g.learn()

    # for tier in g.grammatical:
    #     print('Tier: {}'.format(str(tier)))
    #     print('Grammatical:')
    #     print(g.grammatical[tier])
    #     print('Ungrammatical:')
    #     print(g.ungrammatical[tier])
    #     print()

    dg = g.distill_grammar()
    for tier in dg:
        if len(dg[tier]) > 0:
            print('Prohibited on tier {}:'.format(str(tuple(dg)[0])))
            for seq in dg[tier]:
                print(seq)