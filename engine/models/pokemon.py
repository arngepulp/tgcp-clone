# models/pokemon.py
from engine.models.card import PokemonCard

class PokemonInstance(PokemonCard):
    def __init__(self, card: PokemonCard):
        # Ensure we pull all attributes from the card object
        # If PokemonCard expects a dict, this is fine, but we must ensure 'id' is in there
        super().__init__(card.__dict__ if hasattr(card, '__dict__') else card)
        
        # If the super() call doesn't automatically set self.id, do it manually:
        self.id = getattr(card, 'id', 'unknown-id')
        self.name = getattr(card, 'name', 'Unknown')
        
        self.current_hp = self.hp  
        self.attached_energy = []
        self.status = None
        self.turns_in_play = 0
        self.item = None
        self.ability_used = False
        
    def __repr__(self):
        return f"{self.name} | HP: {self.current_hp}/{self.hp} | Energy: {self.attached_energy} | Status: {self.status} "
        
    def take_damage(self, damage, damage_type):
        if self.weakness:
            for w in self.weakness:
                if w["type"] == damage_type:
                    damage += int(w["value"].replace("+", ""))
        print(f"DEBUG: damage_type={damage_type}, weakness={self.weakness}")
        self.current_hp -= damage
            
        if self.current_hp <= 0:
            self.current_hp = 0 
            pass  # TODO: call game state to handle knockout
    
    def attach_energy(self, energy_type):
        self.attached_energy.append(energy_type)
        
    def advance_turn(self):
        self.turns_in_play += 1
        