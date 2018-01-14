#!/usr/bin/env python3.6
import xml.etree.ElementTree as ET
import json
import copy
import sys
import html

ns = {'svg': '{http://www.w3.org/2000/svg}',
          'html': '"http://www.w3.org/1999/xhtml'}

invisibleAttributes = ["cost", "variables"]
editMetadata = ["type", "target", "priority"]
htmlTags = ["br", "li", "ul"]
template = ET.parse('template.svg')

def genTags(node, tags):
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

def unescape(file):
    print(f"file: {file}")
    text = ""
    with open(file, "r") as f:
        text = f.read();
    new_text = text
    for tag in htmlTags:
        new_text = new_text.replace(f"&lt;{tag}/&gt;", f"<html:{tag}/>")
        new_text = new_text.replace(f"&lt;{tag}&gt;", f"<html:{tag}>")
        new_text = new_text.replace(f"&lt;/{tag}&gt;", f"</html:{tag}>")
    with open(file, "w") as f:
        f.write(new_text)
        
def parseCards(raw_cards):
    cards = {}
    for catagory in raw_cards:
        for (name, subcat) in {name:catagory[name] for name in catagory if name != "name"}.items():
            for card in subcat:
                cards[card["name"]] = card
    return cards

def parseMods(raw_mods):
    mods_dict = parseCards(raw_mods)
    mods_flat = [mod for mods in [mod["code"] for mod in mods_dict.values()] for mod in mods]
    return sorted(mods_flat, key = lambda mod: mod.get("priority", 0), reverse = True)

def doEdit(var, value, target):
    currentValue = target.get(var, "")
    newValue = str(value).replace(f"{{{var}}}", str(currentValue))
    target[var] = newValue
    #print(f"{var}: {currentValue} -> {newValue}")

def applyEditMods(cards_dict, mods):
    edits = [mod for mod in mods if mod["type"] == "edit"]
    for edit in edits:
        target = cards_dict[edit["target"]]
        for (var, value) in {var:edit[var] for var in edit if var not in editMetadata}.items():
            if(var in target):
                doEdit(var, value, target)
            elif(var in target["variables"]):
                doEdit(var, value, target["variables"])
            else:
                raise Exception(f"Edit {edit} could not be applied to card {target} because {var} was not found in the card")

def substituteVariables(cardJSON):
    variables = cardJSON.get("variables", {})

    def subForString(s):
        out = s
        for (var, value) in variables.items():
            out = out.replace(f"{{{var}}}", value)
        #print(out)
        return out
    
    for name, value in cardJSON.items():
        if(not name == "variables"):
            if(isinstance(value, list)):
                cardJSON[name] = [subForString(s) for s in value]
            elif(isinstance(value, str)):
                cardJSON[name] = subForString(value)
    return cardJSON
                

def genCards(cardJSON, modJSON):
    card_svgs = {}
    cards = parseCards(json.loads(open(cardJSON).read()))
    mods = parseMods(json.loads(open(modJSON).read()))

    applyEditMods(cards, mods)
    
    card_template = template.getroot()[0]
    unlabled_elements = ["description", "tags", "name"]
    template.getroot().remove(card_template)

    for (name, card) in cards.items():
        card_svg = copy.deepcopy(card_template)
        card = substituteVariables(card)
        for attribute, value in {attr:card[attr] for attr in card if (attr not in invisibleAttributes)}.items():
            node = card_svg.find(f".//*[@id='{attribute}']")
            if(node.tag == f"{ns['svg']}text"):
                if(attribute == 'name'):
                    node.text = value.capitalize()
                else:
                    node.text = f"{attribute.upper()}: {value}"
            elif(attribute == 'description'):
                list(node)[0].text = value
            elif(attribute == 'tags'):
                    genTags(list(node)[0], value)
        card_svgs[card["name"]] = card_svg
    return card_svgs

def printCards(cardsToPrint, card_svgs):
    for (i, name) in enumerate(cardsToPrint):
        if(not name in card_svgs.keys()):
            raise Exception(f"{name} not found in card names: {card_svgs.keys()}")
        svg = card_svgs[name]
        x = i % 3
        y = i // 3
        svg.set("transform", f"matrix(1 0 0 1 {450 * x} {650 * y})")
        template.getroot().append(svg)
        
    template.write("test.svg")
    unescape("test.svg")

def printAll(card_svgs):
    printCards(card_svgs.keys(), card_svgs)
    
card_svgs = genCards('cards.json', 'feats.json')
printAll(card_svgs)
#printCards(["Drag"], card_svgs)
