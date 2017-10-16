#!/usr/bin/env python3.6
from lib.emote import Emote
import sys

print("Generating Emotes")
Emote().genEmotes('template.svg', 'cards.json', sys.argv[1:])