import itertools
import re

#### Constants -- change these as necessary

SIGMA = ['c', 'v', 'l', 'r', 'b']
MAX_SIZE = 6
PROHIBITIONS = ['<l,r,b>l r', '<l,r,b>r l']
OUTPUT_NAME = 'cvlrb6.txt'


#### Function definitions

def create_constraint_re(constraint):
    tier_search = re.search('\<.*\>', constraint)
    if tier_search:
        tier = constraint[1:len(tier_search.group(0))-1].split(',')
        expression = constraint[len(tier_search.group(0)):]
        return (tier, re.compile(expression))
    else:
        return re.compile(constraint)

def evaluate_constraint(form, constraint):
    exp = create_constraint_re(constraint)
    if isinstance(exp, tuple):
        on_tier = ' '.join([char for char in form if char in exp[0]])
        if exp[1].search(on_tier):
            return True
    else:
        if exp.search(form):
            return True
    return False



#### Action

## Create all possible forms
all_forms = []
for size in range(1, MAX_SIZE+1):
    for form in itertools.product(SIGMA, repeat=size):
        all_forms.append(' '.join(form))

## Remove forms with prohibited sequences
language = []
for form in all_forms:
    violations = [evaluate_constraint(form, prohibition) for prohibition in PROHIBITIONS]
    if not any(violations):
        language.append(form)

## Write to file
with open(OUTPUT_NAME, 'w') as outfile:
    outfile.write('\n'.join(language))