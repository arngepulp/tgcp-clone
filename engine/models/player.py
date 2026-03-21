import sys
import os
import json
import random
from engine.models.card import load_card
# from engine.rules.game_rules import PTS_TO_WIN

def load_deck(path):
    with open(path) as file:
        data = json.load(file)
        
        deck = []
        for card in data["cards"]:
            for _ in range(card["count"]):
                deck.append(card["id"])
        energy = data.get("energy", [])
        return deck, energy
    
def draw_opening_hand(self):
    
    
    # find first basic pokemon
    for i, card_id in enumerate(self.deck):
        card = load_card(card_id)
        if card.evolves_from is None:
            self.hand.append(card_id)
            self.deck.pop(i)
            break
    
    # draw remaining 4
    for _ in range(4):
        self.draw_card()
    
    
class Player:
    def __init__(self, deck_name):
        self.pts = 0
        self.deck_name = deck_name
        self.active = None
        self.bench = [None, None, None]
        self.path = f"decks/{deck_name}.json"
        self.deck, self.energy_types = load_deck(self.path)  # energy_types not energy
        random.shuffle(self.deck)
        self.hand = []          # must exist before draw_opening_hand
        self.discard = []
        self.energy_pool = [random.choice(self.energy_types) for _ in range(2)]
    
        draw_opening_hand(self)  # not self.hand = draw_opening_hand()
    def energy_drawn(self):
        self.energy_pool.pop(0)
        self.energy_pool.append(random.choice(self.energy_types))
        
    def __repr__(self):
        return f"{self.deck_name} | PTS: {self.pts} | Active: {self.active} | Bench: {self.bench} | Energy: {self.energy_pool}"
        
        
        
    def add_pts(self, n):
        self.pts += n
        '''
        if self.pts >= PTS_TO_WIN:
            # TODO win game
            pass
            '''
        
    def draw_card(self):
        new_card = self.deck.pop(0)
        self.hand.append(new_card)
        