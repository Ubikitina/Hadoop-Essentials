#!/usr/bin/env python3

import sys

# Standard Input STDIN
for line in sys.stdin:
  line = line.strip()
  # Divide each line into words
  words = line.split()
  # Each word is written together with a 1 and this is the reducer input
  for word in words:
    print ('%s\t%s' % (word, 1))
