# interfaces/cli/display.py
from engine.game.actions import play_pokemon, attach_energy, attack, retreat, end_turn


def inspect_pokemon(state, location, opponent=False):
    from engine.game.actions import get_location
    
    if opponent:
        # temporarily swap to get opponent's pokemon
        target = state.opponent
    else:
        target = state.current_player
    
    if location == 0:
        pokemon = target.active
    else:
        pokemon = target.bench[location - 1]
    
    if pokemon is None:
        print("No pokemon in that spot!")
        return
    
    print(f"\n{pokemon.name} | HP: {pokemon.current_hp}/{pokemon.hp}")
    print(f"Type: {pokemon.types}")
    print(f"Energy: {pokemon.attached_energy}")
    print(f"Retreat cost: {pokemon.retreat_cost}")
    
    print("\nAttacks:")
    for i, atk in enumerate(pokemon.attacks):
        print(f"  [{i}] {atk['name']} | Cost: {atk['cost']} | Damage: {atk['damage']}")
    
    if pokemon.abilities:
        print("\nAbilities:")
        for ability in pokemon.abilities:
            print(f"  {ability['name']}: {ability['effect']}")
    
    input("\nPress enter to continue...")
    
def choose_action(state):
    print(state)  # print board
    
    print("1. Attack")
    print("2. Play pokemon")
    print("3. Attach energy")
    print("4. Retreat")
    print("5. View hand")
    print("6. Inspect pokemon")
    print("7. End turn")
        
    choice = input("\nChoose action: ")
    
    if choice == "1":
        attack(state)
    elif choice == "2":
        card_id = input("Card ID to play: ")
        location = int(input("Location (0=active, 1-3=bench): "))
        play_pokemon(state, card_id, location)
    elif choice == "3":
        energy = input("Energy type: ")
        location = int(input("Location (0=active, 1-3=bench): "))
        attach_energy(state, energy, location)
    elif choice == "4":
        index = int(input("Bench index to send out (1-3): "))
        retreat(state, index)
    elif choice == "5":
        print("\nYour hand:")
        for i, card_id in enumerate(state.current_player.hand):
            print(f"  [{i}] {card_id}")
        input("\nPress enter to continue...")
    elif choice == "6":
        location = int(input("Location (0=active, 1-3=bench): "))
        who = input("Inspect yours or opponent? (y/o): ")
        inspect_pokemon(state, location, opponent=(who == "o"))
    elif choice == "7":
        end_turn(state)