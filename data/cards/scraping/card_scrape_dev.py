import asyncio
from tcgdexsdk import TCGdex
import json

import sys
sys.path.append('../../../')  

from consts import STAGE_IDS


async def get_one_pokemon(card_id):
    sdk = TCGdex("en") # initializes in english
    
    card = await sdk.card.get(card_id)
    
    if not card: # erorr handling
        print("unable to find card")
        return


    print(f"\nImage URL: {card.image}/high.png")
    
    # get collection in to save to correct file
    collection_id = card.id.split('-')[0]
    
    #card.weaknesses[0].type .val works to
    # im gonna for loop this in case there is ever a cse where multiple weaknesses exist
    weaknesses_list = []
    weaknesses = getattr(card, 'weaknesses', [])

    if weaknesses:
        for w in weaknesses:
            weaknesses_list.append({
                "type": w.type,
                "value": w.value
            })
    else:
        weaknesses = None
        
        
    data = {
        "id": card.id, 
        "name": card.name,
        # get attr is safer, allows for default value if none is found good for dealing with other card types
        "card_type": getattr(card, 'category', 'Pokemon'), 
        "hp": getattr(card, 'hp', 0),
        "types": getattr(card, 'types', []),
    
        "stage": STAGE_IDS[card.stage],
        "evolves_from": getattr(card, 'evolveFrom', None),
        
        "abilities": [
            {
                "name": ability.name,
                "effect_id": getattr(ability, 'effect', None)
            } for ability in getattr(card, 'abilities', []) or []
        ],
        
        "attacks": [
            {
                "name": attack.name,
                "cost": getattr(attack, 'cost', []),
                "damage": getattr(attack, 'damage', "0"), 
                "effect_id": getattr(attack, 'effect', None) 
            } for attack in getattr(card, 'attacks', []) or []
        ],
        
        
        "weakness": weaknesses_list,
        "retreat_cost": getattr(card, 'retreat', 0),
        "rarity": getattr(card, 'rarity', ""),
        
    }
    
    return data, collection_id
    
    
    
    
if __name__ == "__main__":
    card_id = "A1-002"
    card_data, collection_id = asyncio.run(get_one_pokemon(card_id=card_id))
    
    folder = "data/cards/"
    fname = f"{folder}pokemon/{collection_id}/{card_id}.json"
    with open(fname, "w") as file:
        json.dump(card_data, file, indent=2)  
    

