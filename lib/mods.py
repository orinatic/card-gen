from .constants import Constants
from .simplifier import Simplifier

class Mods:
    def parseMods(raw_mods, applicableMods):
        mods_list = []
        
        for catagory in raw_mods:
            for (name, subcat) in {name:catagory[name] for name in catagory if name != "name"}.items():
                for mod in subcat:
                    if(mod["name"] in applicableMods):
                        mods_list.append(mod)

        mods_flat = [mod for mods in [mod["code"] for mod in mods_list] for mod in mods]
        return sorted(mods_flat, key = lambda mod: mod.get("priority", 0), reverse = True)

    def doEdit(var, value, target):
        """Changes the value of var to value, in target card json target"""
        currentValue = target.get(var, "")
        newValue = Simplifier.simplify(str(value).replace(f"{{{var}}}", str(currentValue)))
        target[var] = newValue

    def applyEditMods(cards_dict, mods):
        edits = [mod for mod in mods if mod["type"] == "edit"]
        for edit in edits:
            target = cards_dict[edit["target"]]
            for (var, value) in {var:edit[var] for var in edit if var not in Constants.editMetadata}.items():
                if(var in target):
                    Mods.doEdit(var, value, target)
                elif(var in target["variables"]):
                    Mods.doEdit(var, value, target["variables"])
                else:
                    raise Exception(f"Edit {edit} could not be applied to card {target} because {var} was not found in the card")

    def generateCardList(mods, initialCards):
        cards = {card: 1 for card in initialCards}
        additions = [mod for mod in mods if mod["type"] == "new card"]
        transforms = [mod for mod in mods if mod["type"] == "transform card"]
        for addition in additions:
            for (card, num) in [(card, num) for card, num in addition.items() if not card == "type"]:
                cards[card] = cards.get(card, 0) + num
        for transform in transforms:
            for (old, new) in [(old, new) for old, new in transform.items() if not old == "type"]:
                cards[new] = cards.get(new, 0) + cards.pop(old, 0)
        return cards
