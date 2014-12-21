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


    ## ATTEMPT 2 below
    def distill_grammar(self):
        grammar = defaultdict(list)
        for kfactor in itertools.permutations(self.sigma, 2): # could this consider instead only bigrams prohibited on the segment tier?
            print()
            print(kfactor)
            # ADD: if kfactor not in ungrammatical of tier=kfactor, then check if it's ungrammatical in full_tier
            relevant_tier = self.traverse_lattice(kfactor)
            print('found relevant tier: {}'.format(str(relevant_tier)))
            grammar[relevant_tier].append(kfactor)
        return grammar


    def traverse_lattice(self, kfactor):
        """
        Shower idea: move up lattice from tier=kfactor to full_tier. If ungrammatical on tier=kfactor, result=kfactor-tier.
        If not (meaning that kfactor is grammatical on tier=kfactor), then move up until discovering a tier where kfactor is
        ungrammatical. Move up until a layer of the lattice all considers kfactor grammatical and make result tier the superset of
        the tiers that brought us there; if we never reach a tier where kfactor is grammatical, then result = full_tier
        """

        status = None
        initial_tier = set(kfactor)
        not_in_kfactor = set(self.sigma) - initial_tier

        initial_tier_tuple = tuple(sorted(kfactor))
        if kfactor in self.ungrammatical[initial_tier_tuple]:
            print('returning early') # -> doesn't occur for (V,b) in (V,b)!
            return initial_tier_tuple

        result = initial_tier.copy()
        for char in not_in_kfactor:
            combined_tier = initial_tier.union(set([char]))
            combined_tier_tuple = tuple(sorted(list(combined_tier)))
            if kfactor in self.ungrammatical[combined_tier_tuple]:
                result.add(char)
        return tuple(sorted(list(result)))

    
    # ## ATTEMPT 1 below
    # def distill_grammar(self):
    #     grammar = defaultdict(list)
    #     full_tier = self.tiers[-1]
    #     for kfactor in self.ungrammatical[full_tier]:
    #         print()
    #         print(kfactor)
    #         relevant_tier = self.traverse_lattice(kfactor, full_tier)
    #         print('found relevant tier: {}'.format(str(relevant_tier)))
    #         grammar[relevant_tier].append(kfactor)
    #     return grammar


    # def traverse_lattice(self, kfactor, start_tier):
    #     """Find the largest tier on which a restriction fails to hold and use it to infer the restriction's proper tier
    #     """
    #     for size in reversed(range(len(start_tier))):
    #         for tier in itertools.combinations(start_tier, size):
    #             if kfactor[0] in tier and kfactor[1] in tier:
    #                 print(tier)
    #                 if kfactor in self.grammatical[tier]:
    #                     print('grammatical here')
    #                     residue = set(tier) - set(kfactor)
    #                     return tuple(sorted(list(set(start_tier) - residue)))
    #     raise Exception('Lattice traversal has failed.')


    def tiers_equal(tier1, tier2):
        return set(tier1) == set(tier2)
        

    def get_ngrams(self, sequence, max_k):
        return list(itertools.chain.from_iterable([zip(*[sequence[i:] for i in range(n)]) for n in range(max_k+1)]))


if __name__ == '__main__':
    g = Grammar('cvlrb6.txt')

    g.learn()

    # for tier in g.grammatical:
    #     print('Tier: {}'.format(str(tier)))
    #     print('Grammatical:')
    #     print(g.grammatical[tier])
    #     print('Ungrammatical:')
    #     print(g.ungrammatical[tier])
    #     print()

    gr = g.distill_grammar()
    # for tier in gr:
    #     print()
    #     print(tier)
    #     print(gr[tier])



    ## Is the if check below here still appropriate?
    # print('UNGRAMMATICAL:')
    # for t in g.ungrammatical:
    #     if len(g.ungrammatical[t]) < ((len(t))**2+len(t)):
    #         print(t)
    #         print(g.ungrammatical[t])
    #         print()