import json
from .cards import Cards
from .mods import Mods

class Characters:
    def __init__(self, template, charactersJSON, cardsJSON, modsJSON):
        self.chars = self.parseCharacters(charactersJSON)
        self.cardMaker = Cards(template, cardsJSON)
        self.cardsJSON = cardsJSON
        self.modsJSON = modsJSON
        
    def parseCharacters(self, charactersJSON):
        chars = json.loads(open(charactersJSON).read())
        return { char["name"]:char for char in chars }

    
    def genCharacter(self, name):
        if not name in self.chars:
            raise Exception(f"name {name} not in character list {self.chars.keys()}")
        modNames = self.chars[name].get("modifiers", [])
        cardNames = self.chars[name]["cards"]

        mods = Mods.parseMods(json.loads(open(self.modsJSON).read()), modNames)
        cardsToNumbers = Mods.generateCardList(mods, cardNames)

        cards = self.cardMaker.genCards(name, cardsToNumbers.keys(), mods) 
        
        return {cards[name]:cardsToNumbers[name] for name in cards.keys()} 
        
        
    def printCharacters(self, names):
        cardsByChar = [self.genCharacter(name) for name in names]
        cardsToPrint = {}
        for character in cardsByChar: 
            for(card, num) in character.items():
                cardsToPrint[card] = cardsToPrint.get(card, 0) + num
        self.cardMaker.printAll(cardsToPrint)
            
    def printAll(self):
        self.printCharacters(self.chars.keys())
