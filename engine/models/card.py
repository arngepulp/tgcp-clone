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