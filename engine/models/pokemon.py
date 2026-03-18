# models/pokemon.py
from models.card import PokemonCard

class PokemonInstance(PokemonCard):
    def __init__(self, card):
        super().__init__(card.__dict__)
        
        self.current_hp = self.hp  
        self.attached_energy = []
        self.status = None
        self.turns_in_play = 0
        self.item = None
        
    def health_change(self, change):
        self.current_hp += change
        if self.current_hp <= 0:
            self.current_hp = 0 
            pass  # TODO: call game state to handle knockout
    
    def attach_energy(self, energy_type):
        self.attached_energy.append(energy_type)
        
    def advance_turn(self):
        self.turns_in_play += 1