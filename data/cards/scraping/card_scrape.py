# card_scrape.py
import asyncio
import json
import os
from tcgdexsdk import TCGdex
from tcgdexsdk.enums import Quality, Extension
from consts import STAGE_IDS, ENERGY_NAMES_TO_SYMBOLS
from data.cards.scraping.get_image_test import save_placeholder_image

def convert_energy_cost(cost_list):
    if not cost_list:
        return []
    return [ENERGY_NAMES_TO_SYMBOLS.get(energy, energy) for energy in cost_list]

def save_image(image_response, filepath):
    image_bytes = image_response.read()
    with open(filepath, "wb") as file:
        file.write(image_bytes)

async def fetch_and_save_all_tcgp():
    sdk = TCGdex("en")
    series_id = "tcgp"
    
    series = await sdk.serie.get(series_id)
    if not series:
        print("failed to find tcgp")
        return
    
    for set_resume in series.sets:
        full_set = await sdk.set.get(set_resume.id)
        print(f"\nProcessing Set: {full_set.name} ({len(full_set.cards)} cards)")
        
        for card_resume in full_set.cards:
            card_id = card_resume.id
            
            try:
                card_data, collection_id, card_type = await get_one_pokemon_details(sdk, card_id)
                
                folder = f"data/cards/{card_type}/{collection_id}/metadata"
                image_folder = f"data/cards/{card_type}/{collection_id}/image"
                fname = f"{folder}/{card_id}.json"
                if os.path.exists(fname):
                    print(f"Skipping {card_id} - already saved")
                    continue
                
                os.makedirs(folder, exist_ok=True)
                os.makedirs(image_folder, exist_ok=True)
                
                # save metadata
                fname = f"{folder}/{card_id}.json"
                with open(fname, "w") as file:
                    json.dump(card_data, file, indent=2)
                
                image_response = card_resume.get_image(Quality.HIGH, Extension.PNG)
                image_path = f"{image_folder}/{card_id}.png"
                if image_response is not None:
                    save_image(image_response, image_path)
                else:
                    save_placeholder_image(card_resume, image_path)
                    
                print(f"Saved {card_id}: {card_data['name']}")
                
                
            except Exception as e:
                print(f"Failed to scrape {card_id}: {e}")

async def get_one_pokemon_details(sdk, card_id):
    card = await sdk.card.get(card_id)
    if not card:
        raise ValueError("Card not found")
    
    collection_id = card.id.split('-')[0]
    card_type = getattr(card, "category", "").lower()
    
    if not card_type:
        raise ValueError("No card type found")
    
    weaknesses_list = []
    weaknesses = getattr(card, 'weaknesses', [])
    if weaknesses:
        for w in weaknesses:
            weaknesses_list.append({"type": w.type, "value": w.value})
    
    data = {
        "id": card.id,
        "name": card.name,
        "suffix": getattr(card, 'suffix', None),
        "card_type": getattr(card, 'category', 'Pokemon'),
        "hp": getattr(card, 'hp', 0),
        "types": getattr(card, 'types', None) or [],
        "stage": STAGE_IDS.get(card.stage, None),
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
                "cost": convert_energy_cost(getattr(at, 'cost', [])),
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