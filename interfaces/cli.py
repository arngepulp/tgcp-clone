# interfaces/cli/display.py
from engine.game.actions import play_pokemon, attach_energy, attack, retreat, end_turn, evolve_pokemon
from engine.models.card import load_card, PokemonCard


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
    print("3. Evolve Pokemon")
    print("4. Attach energy")
    print("5. Retreat")
    print("6. View hand")
    print("7. Inspect pokemon")
    print("8. End turn")
        
    choice = input("\nChoose action: ")
    ## TODO add reprompts on failure, works with adding return TRUE for actions to see if they succeeded or not
    if choice == "1":
        # print players attacks and list indexes for each
        atk_options = state.current_player.active.attacks
        for i in atk_options:
            print(f"{i}). {atk_options[i]}")
        index = int(input("\n What attack?"))
        attack(state,index)
        
    elif choice == "2":
        card_id = input("Card ID to play: ")
        location = int(input("Location (0=active, 1-3=bench): "))
        play_pokemon(state, card_id, location)
        
    elif choice == "3":
            # find all evolvable pokemon on board
        evolvable = []
        if state.current_player.active and state.current_player.active.turns_in_play >= 1:
            evolvable.append((0, state.current_player.active))
        for i, p in enumerate(state.current_player.bench):
            if p and p.turns_in_play >= 1:
                evolvable.append((i + 1, p))
        
        if not evolvable:
            print("No pokemon can evolve yet!")
            input("Press enter to continue...")
        else:
            # find cards in hand that evolve from something on board
            board_names = [p.name for _, p in evolvable]
            valid_evolvers = []
            for card_id in state.current_player.hand:
                card = load_card(card_id)
                if card.evolves_from in board_names:
                    valid_evolvers.append(card_id)
            
            if not valid_evolvers:
                print("No evolution cards in hand!")
                input("Press enter to continue...")
            else:
                print("\nEvolve with:")
                for i, card_id in enumerate(valid_evolvers):
                    print(f"  [{i}] {card_id}")
                evolver_id = valid_evolvers[int(input("Choose: "))]
                
                evolver_card = load_card(evolver_id)
                targets = [(loc, p) for loc, p in evolvable if p.name == evolver_card.evolves_from]
                
                if len(targets) == 1:
                    location = targets[0][0]
                else:
                    print("\nEvolve which pokemon?")
                    for i, (loc, p) in enumerate(targets):
                        print(f"  [{i}] {'Active' if loc == 0 else f'Bench {loc}'}: {p.name}")
                    location = targets[int(input("Choose: "))][0]
                
                evolve_pokemon(state, location, evolver_id)
        
        
    elif choice == "4":
        location = int(input("Location (0=active, 1-3=bench): "))
        attach_energy(state,location)
        
    elif choice == "5":
        index = int(input("Bench index to send out (1-3): "))
        retreat(state, index)
    elif choice == "6":
        print("\nYour hand:")
        for i, card_id in enumerate(state.current_player.hand):
            print(f"  [{i}] {card_id}")
        input("\nPress enter to continue...")
        
    elif choice == "7":
        location = int(input("Location (0=active, 1-3=bench): "))
        who = input("Inspect yours or opponent? (y/o): ")
        inspect_pokemon(state, location, opponent=(who == "o"))
    elif choice == "8":
        end_turn(state)