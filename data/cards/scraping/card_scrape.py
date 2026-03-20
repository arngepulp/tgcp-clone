# card_scrape.py
import asyncio
import json
import os
import sys
from tcgdexsdk import TCGdex

# run with python -m data.cards.scraping.card_scrape
#sys.path.append('../../../')  
from consts import STAGE_IDS

async def fetch_and_save_all_tcgp():
    sdk = TCGdex("en")
    series_id = "tcgp"
    
    # getting series details
    series = await sdk.serie.get(series_id)
    if not series:
        print("failed to find tgcp")
        return


    for set_resume in series.sets:
        # fetch all the cards
        full_set = await sdk.set.get(set_resume.id)
        print(f"\nProcessing Set: {full_set.name} ({len(full_set.cards)} cards)")

        for card_resume in full_set.cards:
            card_id = card_resume.id
            
            
            # grad detail for one card
            try:
                card_data, collection_id, card_type = await get_one_pokemon_details(sdk, card_id)
                
                
                folder = f"data/cards/{card_type}/{collection_id}/metadata"
                os.makedirs(folder, exist_ok=True)
                
                fname = f"{folder}/{card_id}.json"
                with open(fname, "w") as file:
                    json.dump(card_data, file, indent=2)
                
                print(f"Saved {card_id}: {card_data['name']}")
                
                # idk if theres cloudfare or something its an api tho??
                await asyncio.sleep(0.1) 
                
            except Exception as e:
                print(f"Failed to scrape {card_id}: {e}")


async def get_one_pokemon_details(sdk, card_id):
    card = await sdk.card.get(card_id)
    if not card:
        raise ValueError("Card not found")

    collection_id = card.id.split('-')[0]
    
    card_type = getattr(card, "category", "")
    card_type = card_type.lower()
    if not card_type:
        print("no card type found. error")
        return
    
    # Handle Weaknesses
    weaknesses_list = []
    weaknesses = getattr(card, 'weaknesses', [])
    if weaknesses:
        for w in weaknesses:
            weaknesses_list.append({"type": w.type, "value": w.value})

    # Build Metadata
    data = {
        "id": card.id, 
        "name": card.name,
        "card_type": getattr(card, 'category', 'Pokemon'), 
        "hp": getattr(card, 'hp', 0),
        "types": getattr(card, 'types', []),
        # Use your STAGE_IDS mapping from consts.py
        "stage": STAGE_IDS.get(card.stage, card.stage), 
        "evolves_from": getattr(card, 'evolveFrom', None),
        "abilities": [
            {
                "name": ab.name,
                "effect_id": getattr(ab, 'effect', None)
            } for ab in getattr(card, 'abilities', []) or []
        ],
        "attacks": [
            {
                "name": at.name,
                "cost": getattr(at, 'cost', []),
                "damage": getattr(at, 'damage', "0"), 
                "effect_id": getattr(at, 'effect', None) 
            } for at in getattr(card, 'attacks', []) or []
        ],
        "weakness": weaknesses_list,
        "retreat_cost": getattr(card, 'retreat', 0),
        "rarity": getattr(card, 'rarity', ""),
        "image_path": f"{card.image}/high.png"
    }
    
    return data, collection_id, card_type

if __name__ == "__main__":
    asyncio.run(fetch_and_save_all_tcgp())