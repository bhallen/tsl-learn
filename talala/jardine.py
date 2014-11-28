import csv
from collections import defaultdict
import itertools


#### FUNCTIONS

def find_ngrams(input, n):
  return zip(*[input[i:] for i in range(n)])

def get_paths(item):
    paths = []
    for left in range(len(item)-1):
        for right in range(left+1,len(item)):
            paths.append((item[left], tuple(item[left+1:right]), item[right]))
    return paths

def select_tier_paths(paths, tier):
    def on_tier(path):
        return every()
    return set([p for p in paths if all([s in tier for s in p[1]])])

    

#### INIT

with open('training.txt') as tfile:
    reader = csv.reader(tfile, delimiter='\t')
    training = [line[0].split(' ') for line in reader]

sigma = set([segment for item in training for segment in item])

paths = defaultdict(int)
for item in training:
    for p in get_paths(['#']+item+['#']):
        paths[p] += 1

tier = sigma.copy()

subs = set()


#### FIND TIER

looking = True
while looking:
    for s1 in tier:
        print('s1: {}'.format(s1))
        s1_removable = True
        tier_with_edges = tier.copy()
        tier_with_edges.add('#')
        for s2 in tier_with_edges-set(s1): # sure we need to remove s1 here?
            print('s2: {}'.format(s2))
            antitier = sigma-tier_with_edges
            antitier_paths = select_tier_paths(paths,antitier)
            antitier_bigrams = [(p[0],p[2]) for p in antitier_paths]
            if (s1,s2) not in antitier_bigrams or (s2,s1) not in antitier_bigrams:
                s1_removable = False
                print('failed test 1')
            else:
                non_s1_segment_pairs = list(itertools.product(tier_with_edges-set(s1), repeat=2)) # not 100% sure this is the right place to remove s1
                for nssp in non_s1_segment_pairs:
                    spans = [p[1] for p in paths if p[0]==nssp[0] and p[2]==nssp[1]]
                    if any([all([segment == s1 for segment in span]) for span in spans]) and not any([not all([segment == s1 for segment in span]) for span in spans]): # also unsure about second term here
                        s1_removable = False
                        print('failed test 2')
        if s1_removable:
            tier = tier-set(s1)
            break
    looking = False

print(tier)

