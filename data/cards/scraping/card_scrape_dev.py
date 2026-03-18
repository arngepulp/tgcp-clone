import asyncio
from tcgdexsdk import TCGdex

async def get_one_pokemon(card_id):
    sdk = TCGdex("en")
    
    card = await sdk.card.get(card_id)
    
    if not card: # erorr handling
        print("unable to find card")
        return

    # testing if i get anything cool!
    print(card.name)
    print(f"ID: {card.id}")
    
    hp = getattr(card, 'hp', 'N/A')
    types = getattr(card, 'types', [])
    print(f"\nImage URL: {card.image}/high.png")
    
    print(card.__dict__)

if __name__ == "__main__":
    asyncio.run(get_one_pokemon("A1-001"))