import xml.etree.ElementTree as ET
import copy
import re
from .constants import Constants

class Diff:
  def __init__(self):
    self.processed = False
    self.previosuCards = []
    self.addedCards = []
    self.removedCards = []

  def getCards(self, svg):
    body = svg.getroot()[0]
    cards = []
    for svg in body: 
      for card in svg:
        cards.append(card)
    return cards

  def unescapeText(text):
    new_text = text
    for tag in Constants.htmlTags:
      new_text = new_text.replace(f"&lt;{tag}/&gt;", f"<html:{tag}/>")
      new_text = new_text.replace(f"&lt;{tag}&gt;", f"<html:{tag}>")
      new_text = new_text.replace(f"&lt;/{tag}&gt;", f"</html:{tag}>")
      new_text = new_text.replace(" ", "")
      new_text = re.sub("transform=\"matrix\(\d+\)\"", "", new_text)

    return new_text

  def parseOriginal(self, previous):
    try:
      previous = ET.parse(previous)
      self.previousCards = self.getCards(previous)
    except:
      print("failed to parse")
      self.previousCards = []
   

  def process(self, newCards):
    def cardEq(a, b):
      aTxt = Diff.unescapeText(str(ET.tostring(a)))
      bTxt = Diff.unescapeText(str(ET.tostring(b)))
      return  aTxt == bTxt

    self.processed = True
    self.addedCards = []
    unfoundPrevCards = copy.copy(self.previousCards)
    for newCard in newCards:
      originalCard = next((c for c in unfoundPrevCards if cardEq(newCard, c)), None)
      if(originalCard is None):
        self.addedCards.append(newCard)
      else:
        unfoundPrevCards.remove(originalCard)
    self.removedCards = unfoundPrevCards

  def getAddedCards(self, newCards):
    if(not self.processed):
      self.process(newCards)
    return self.addedCards

  def getRemovedCards(self, newCards):
    if(not self.processed):
      self.process(newCards)
    return self.removedCards