#!/usr/bin/env python3.6
from lib.characters import Characters
from lib.cards import Cards
print("Generating cards")

chars = Characters('template.svg', 'characters.json', 'cards.json', 'feats.json')

chars.printAll()
