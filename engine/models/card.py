# models/card.py
import json

class Card:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.card_type = data["card_type"]

    @classmethod
    def from_json(cls, filepath):
        with open(filepath) as f:
            data = json.load(f)
        return cls(data)
    
def load_card(card_id):
    parts = card_id.split("-")
    set_id = parts[0]
    filepath = f"data/cards/pokemon/{set_id}/metadata/{card_id}.json"
    
    with open(filepath) as f:
        data = json.load(f)
    
    if data["card_type"] == "Pokemon":
        return PokemonCard(data)
    elif data["card_type"] == "Trainer":
        return TrainerCard(data)
    else:
        return Card(data)    


class PokemonCard(Card):
    def __init__(self, data: dict):
        super().__init__(data)
        self.hp = data["hp"]
        self.types = data["types"]
        self.stage = data["stage"]
        self.evolves_from = data.get("evolves_from", None)
        self.abilities = data.get("abilities", None)
        self.attacks = data.get("attacks", [])
        self.weaknesses = data.get("weaknesses", None)
        self.retreat_cost = data.get("retreat_cost", 0)


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