import json
import copy
from .cards import Cards
from .mods import Mods

class Emote:
    def genEmotes(self, template: str, cardsJSON: str, emoteTypes:list):
        cardMaker = Cards(template, cardsJSON)
        
        emoteJSONTemplates = cardMaker.parseCards(json.loads(open(cardsJSON).read()), ["1 {Emote}", "2 {Emote}", "5 {Emote}"])
        emoteJSONs = []

        for (_, card) in emoteJSONTemplates.items():
            for emoteType in emoteTypes:
                emoteCard = copy.deepcopy(card)
                Mods.doEdit("Emote", emoteType, emoteCard["variables"])
                emoteJSONs.append(emoteCard)

        emoteSVGs = cardMaker.doGenCards("EMOTES", emoteJSONs).values()

        cardMaker.printAll({card:3 for card in emoteSVGs}, 'emotes.svg')


        


