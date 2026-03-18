import asyncio
from tcgdexsdk import TCGdex
import json

async def main(): # idk what this is but its what the docuementation uses
    # Init the SDK in english
    sdk = TCGdex("en")

    series_data = await sdk.serie.get("tcgp")
    
   
    if series_data:
        print(f"Successfully fetched: {series_data.name}")
        for card_set in series_data.sets:
            print(f"Set: {card_set.name} (ID: {card_set.id})")
    else:
        print("No series found.")
    

if __name__ == "__main__":
    asyncio.run(main())