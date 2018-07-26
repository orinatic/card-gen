#!/usr/bin/env python3.6
import xml.etree.ElementTree as ET
import json
import sys
import html
import string
from .constants import Constants
from .mods import Mods
from .template_service import TemplateService

class Cards:
    def __init__(self, template, cardsJSON):
        self.ts = TemplateService(template)
        self.cardsJSON = cardsJSON
    
    def genTags(self, node, tags):
        def iter(node, tags, first):
            if(tags == []):
                return
            elif(first):
                node.text = tags[0]
                iter(node, tags[1:], False)
            else:
                br = ET.SubElement(node, 'html:br')
                br.tail = tags[0]
                iter(node, tags[1:], False)
        iter(node, tags, True)


    def parseCards(self, raw_cards: dict, cardsList: list):
        """Takes dictionary of raw cards and a list of cards to parse, and returns a dictionary
        of name->card json"""
        cards = {}
        toParse = list(cardsList)
        for catagory in raw_cards:
            for (name, subcat) in {name:catagory[name] for name in catagory if name != "name"}.items():
                for card in subcat:
                    if(card["name"]) in cardsList:
                        toParse.remove(card["name"])
                        cards[card["name"]] = card
        if(len(toParse) > 0):
            raise Exception(f"Could not find cards {toParse}. List was {cardsList}")
        return cards

    def substituteVariables(self, cardJSON):
        variables = cardJSON.get("variables", {})

        def subForString(s):
            out = s
            for (var, value) in variables.items():
                out = out.replace(f"{{{var}}}", value)
            return out

        for name, value in cardJSON.items():
            if(not name == "variables"):
                if(isinstance(value, list)):
                    cardJSON[name] = [subForString(s) for s in value]
                elif(isinstance(value, str)):
                    cardJSON[name] = subForString(value)
        return cardJSON

    # returns map of card names to card svg code
    def genCards(self, characterName, cardNames, mods):
        cards = self.parseCards(json.loads(open(self.cardsJSON).read()), cardNames)
        Mods.applyEditMods(cards, mods)
        return self.doGenCards(characterName, cards.values())

    def doGenCards(self, characterName, cardJSONS: list):
        """Returns name -> svg"""
        card_svgs = {}
        for (card) in cardJSONS:
            card_svg = self.ts.getNewCard()
            card = self.substituteVariables(card)
            for attribute, value in {attr:card[attr] for attr in card}.items():
                node = card_svg.find(f".//*[@id='{attribute}']")
                if(node.tag == f"{Constants.ns['svg']}text"):
                    if(attribute == 'name'):
                        node.text = string.capwords(value)
                    else:
                        node.text = f"{attribute.upper()}: {value}"
                elif(attribute == 'description'):
                    list(node)[0].text = value
                elif(attribute == 'tags'):
                        self.genTags(list(node)[0], value)
                node = card_svg.find(f".//*[@id='Character Name']")
                node.text = characterName.upper()
                card_svgs[card["name"]] = card_svg
        return card_svgs
                
    def printAll(self, cards, output):
        """Takes a dictionary of cards->number of times to print"""
        for (card, num) in cards.items():
            self.ts.addCards(card, num)
        self.ts.writeCards(output)
