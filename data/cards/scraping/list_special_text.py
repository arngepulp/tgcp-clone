from engine.models.card import load_card
import os

# load from a1
directory = "data/cards/pokemon/A1/metadata"
files = os.listdir(directory)
files = [f for f in files if os.path.isfile(directory+'/'+f)]
files = [f.split('.')[0] for f in files]

attack_effects = []
abilities = []
for f in files:
    card = load_card(f)
    # Use append instead of =
    attack_effects.append(card.attacks[0]["effect_id"])
    if card.abilities:
        for ab in card.abilities:
            abilities.append(ab["effect_id"])
    
attack_effects = [a for a in attack_effects if a is not None]
print(abilities)
print(attack_effects)
# unique_effects = list(set(attack_effects))
# print(f"Total effects found: {len(attack_effects)}")
# print(f"Unique effect IDs: {unique_effects}")