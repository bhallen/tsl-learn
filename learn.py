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
        """
        self.tiers = list(itertools.chain.from_iterable(itertools.combinations(self.sigma, r) for r in range(1,len(self.sigma)+1)))


    # def find_informative_tiers(self):
    #     informative_tiers = []
    #     for t_sub in self.tiers:
    #         for t_super in self.tiers:
    #             if t_sub < t_super:
    #                 if len(t_sub)**2 + len(t_sub) - len(self.grammatical[t_sub]) > len(t_super)**2 + len(t_super) - len(self.grammatical[t_super]):
    #                     informative_tiers.append(t_sub)
    #                     break

    #     print('INFORMATIVE TIERS BELOW:')
    #     for t in informative_tiers:
    #         print(t)
    #         print('Grammatical in this tier:')
    #         print(g.grammatical[t])
    #         print('Ungrammatical in this tier:')
    #         print(g.ungrammatical[t])
    #         print()


    def get_ngrams(self, sequence, max_k):
        return list(itertools.chain.from_iterable([zip(*[sequence[i:] for i in range(n)]) for n in range(max_k+1)]))


if __name__ == '__main__':
    g = Grammar('datasets/training_unbounded_harm_restricted.txt')

    g.learn()

    for tier in g.grammatical:
        print('Tier: {}'.format(str(tier)))
        print('Grammatical:')
        print(g.grammatical[tier])
        print('Ungrammatical:')
        print(g.ungrammatical[tier])
        print()

    
    ## Is the if check below here still appropriate?
    # print('UNGRAMMATICAL:')
    # for t in g.ungrammatical:
    #     if len(g.ungrammatical[t]) < ((len(t))**2+len(t)):
    #         print(t)
    #         print(g.ungrammatical[t])
    #         print()

    # g.find_informative_tiers()