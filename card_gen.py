#!/usr/bin/env python3.6
from lib.characters import Characters
from lib.cards import Cards
import sys
print("Generating cards")

chars = Characters('template.svg', 'characters.json', 'cards.json', 'feats.json')

if(len(sys.argv) > 1):
  chars.printCharacters(sys.argv[1:], 'test.svg')
else:
  chars.printAll('test.svg')
