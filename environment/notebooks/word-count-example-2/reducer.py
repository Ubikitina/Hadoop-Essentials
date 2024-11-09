#!/usr/bin/env python3

from collections import defaultdict
import sys

# We use a dictionary for words with an integer as a value
word_counter = defaultdict(int)

# For each line we count the total number of appearances
for line in sys.stdin:
    word, number = line.strip().split('\t')
    word_counter[word] += int(number)

# We write for each word the total number of occurrences
for word in sorted(word_counter.keys()):
    print ('%s\t%s' % (word_counter[word], word))
