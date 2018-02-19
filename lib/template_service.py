import xml.etree.ElementTree as ET
import copy
from .constants import Constants
from .diff import Diff

class TemplateService:
    def __init__(self, template):
        self.diff = Diff()
        self.cards = []
        self.template = ET.parse(template)

        self.cardTemplate = self.template.getroot()[0][0][0]
        self.template.getroot()[0][0].remove(self.cardTemplate)

        self.pageTemplate = self.template.getroot()[0][0]
        self.template.getroot()[0].remove(self.pageTemplate)

        self.currentPage = copy.deepcopy(self.pageTemplate)

        self.finishedPages = []

    def unescape(file):
        text = ""
        with open(file, "r") as f:
            text = f.read()
        new_text = text
        for tag in Constants.htmlTags:
            new_text = new_text.replace(f"&lt;{tag}/&gt;", f"<html:{tag}/>")
            new_text = new_text.replace(f"&lt;{tag}&gt;", f"<html:{tag}>")
            new_text = new_text.replace(f"&lt;/{tag}&gt;", f"</html:{tag}>")
        with open(file, "w") as f:
            f.write(new_text)
        
    def getNewCard(self):
        return copy.deepcopy(self.cardTemplate)

    def addCard(self, card):
        self.cards.append(copy.deepcopy(card))
    
    def addCards(self, card, num):
        for i in range(num):
            self.addCard(card)

    def addCardToSVG(self, card):
        n = len(list(self.currentPage))
        if(n == 9):
            self.finishedPages.append(self.currentPage)
            self.currentPage = copy.deepcopy(self.pageTemplate)
            n = 0
        x = n % 3
        y = n // 3
        card.set("transform", f"matrix(1 0 0 1 {450 * x} {650 * y})")
        self.currentPage.append(card)
    
    def addCardsToSVG(self, card, num):
        for i in range(num):
            self.addCard(copy.deepcopy(card))

    def writeCards(self, target):
        self.diff.parseOriginal("lastprint.svg")
        for card in self.diff.getAddedCards(self.cards):
            self.addCardToSVG(card)
        for card in self.diff.getRemovedCards(self.cards):
            print(f"removed card from {card[4].text}: {card[1].text}")

        self.finishedPages.append(self.currentPage)
        for page in self.finishedPages:
            self.template.getroot()[0].append(page)
        self.finishedPages = []
        self.template.write(target)
        TemplateService.unescape(target)
