#!/usr/bin/env python3.6
from lib.characters import Characters
from lib.cards import Cards
from lib.diff import Diff
import sys
print("Generating cards")

chars = Characters('template.svg', 'characters.json', 'cards.json', 'feats.json')

output = 'test.svg'

diff = Diff()

diff.parseOriginal(output)

if(len(sys.argv) > 1):
  chars.printCharacters(sys.argv[1:], output)
else:
  chars.printAll(output)
