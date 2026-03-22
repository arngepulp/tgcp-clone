# models/card.py
import json, os

class Card:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.card_type = data["card_type"]
        self.rarity = data.get("rarity", None)

    @classmethod
    def from_json(cls, filepath):
        with open(filepath) as f:
            data = json.load(f)
        return cls(data)
    
def load_card(card_id):
    parts = card_id.split("-")
    set_id = parts[0]
    
    # try pokemon first, then trainer
    for card_type in ["pokemon", "trainer"]:
        filepath = f"data/cards/{card_type}/{set_id}/metadata/{card_id}.json"
        if os.path.exists(filepath):
            with open(filepath) as f:
                data = json.load(f)
            if data["card_type"] == "Pokemon":
                return PokemonCard(data)
            elif data["card_type"] == "Trainer":
                return TrainerCard(data)
            else:
                return Card(data)
    
    raise FileNotFoundError(f"Card {card_id} not found in any folder")
    
def load_all_cards():
    cards = []
    for card_type in ["pokemon", "trainer"]:
        base = f"data/cards/{card_type}"
        if not os.path.exists(base):
            continue
        for set_folder in os.listdir(base):
            metadata_path = os.path.join(base, set_folder, "metadata")
            if not os.path.exists(metadata_path):
                continue
            for fname in os.listdir(metadata_path):
                if fname.endswith(".json"):
                    card_id = fname.replace(".json", "")
                    try:
                        card = load_card(card_id)
                        cards.append(card)
                    except Exception as e:
                        print(f"Failed to load {card_id}: {e}")
    return cards

def filter_cards(cards, type_filter=None, min_hp=0, max_hp=999, 
                 has_ability=False, set_filter=None, is_ex=False, 
                 is_trainer=False, search=None, rarity = None):
    result = cards
    
    if search:
        search = search.lower()
        result = [c for c in result if search in c.name.lower()]
    
    if type_filter:
        result = [c for c in result if hasattr(c, 'types') and c.types and type_filter in c.types]
    
    if set_filter:
        result = [c for c in result if c.id.startswith(set_filter)]
    
    if is_trainer:
        result = [c for c in result if c.card_type == "Trainer"]
    else:
        result = [c for c in result if hasattr(c, 'hp')]
        if min_hp:
            result = [c for c in result if c.hp and c.hp >= min_hp]
        if max_hp < 999:
            result = [c for c in result if c.hp and c.hp <= max_hp]
        if has_ability:
            result = [c for c in result if hasattr(c, 'abilities') and c.abilities]
        if is_ex:
            result = [c for c in result if c.suffix == "EX"]
            
    if rarity:
        print(f"DEBUG rarity filter: rarity='{rarity}', sample rarity='{result[0].rarity if result else 'no cards'}'")
        result = [c for c in result if hasattr(c, 'rarity') and c.rarity == rarity]

    return result


class PokemonCard(Card):
    def __init__(self, data: dict):
        super().__init__(data)
        self.hp = data["hp"]
        self.types = data["types"]
        self.stage = data["stage"]
        self.evolves_from = data.get("evolves_from", None)
        self.abilities = data.get("abilities", None)
        self.attacks = data.get("attacks", [])
        self.weakness = data.get("weakness", None)
        self.retreat_cost = data.get("retreat_cost", 0)
        self.prefix = data.get("prefix",None)


class TrainerCard(Card):
    def __init__(self, data: dict):
        super().__init__(data)
        pass  # TODO
    
class ToolCard(Card):
    def __init__(self, data: dict):
        super().__init__(data)
        pass  # TODO
    
class StageCard(Card):
    def __init__(self, data: dict):
        super().__init__(data)
        pass  # TODO