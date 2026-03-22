from engine.models.card import load_card, PokemonCard
from engine.models.pokemon import PokemonInstance
from collections import Counter
from engine.game.effects import resolve_effects

def check_requirements(target, check, wildcard='{C}'):
    # count frequency of items in each list
    target_counts = Counter(target)
    check_counts = Counter(check)
    
    # find amount of wildcards
    wildcards_needed = target_counts.pop(wildcard, 0)
    
    # check for all matching
    for item, required_amount in target_counts.items():
        if check_counts[item] < required_amount:
            return False 
        
        
        check_counts[item] -= required_amount
        
    leftover_items = sum(check_counts.values())
    
    return leftover_items >= wildcards_needed

def get_location(state_or_player, location):
    # This checks if the first argument is the whole game or just a player
    if hasattr(state_or_player, 'current_player'):
        player = state_or_player.current_player
    else:
        player = state_or_player

    if location == 0:
        return player.active
    else:
        # Extra safety check for bench index
        try:
            return player.bench[location - 1]
        except (IndexError, AttributeError):
            return None

def play_pokemon(state, card_id, location, forced_player=None):
    player = forced_player if forced_player else state.current_player
    
 
    if player.active is None and location != 0:
        print("Illegal move: Must place Active Pokémon first!")
        return False

    if get_location(player, location) is not None:
        print("That spot is already taken!")
        return False 
    
    card = load_card(card_id)
    pokemon = PokemonInstance(card)
    
    if getattr(pokemon, 'evolves_from', None) is not None:
        print("This is not a basic pokemon!")
        return False
    
    # Placement
    if location == 0:
        player.active = pokemon
    else:
        player.bench[location - 1] = pokemon
    
    if card_id in player.hand:
        player.hand.remove(card_id)
    
    return True

    
def attach_energy(state,location=0):
    if state.first_turn and state.phase != 'setup':
        print("Can't attach energy on the first turn!")
        return False
    
    if state.current_player.energy_attached_this_turn:
        print("Already attached energy this turn!")
        return False
    instance = get_location(state, location)
    if instance is None:
        print("No pokemon in that spot!")
        return
    instance.attach_energy(state.current_player.energy_pool[0])
    state.current_player.energy_attached_this_turn = True
    print(f"the value {state.current_player.energy_attached_this_turn}")
    state.current_player.energy_drawn()
    
def evolve_pokemon(state, location, evolver_id):
    # 1. Get the current player and the target
    player = state.current_player
    evolvee = get_location(player, location)
    
    if evolvee is None:
        return False
    
    # 2. RULE: Can't evolve the same turn it was played
    if evolvee.turns_in_play < 1:
        print("This pokemon hasn't been out long enough!")
        return False
    
    # 3. RULE: Can't evolve the same pokemon twice in one turn
    if getattr(evolvee, 'evolved_this_turn', False):
        print("This pokemon already evolved this turn!")
        return False
    
    # 4. Check if proper evolves from
    evolver_card = load_card(evolver_id)
    if getattr(evolver_card, 'evolves_from', None) != evolvee.name:
        print("Incorrect evolution line!")
        return False
    
     # store old state
    energy = evolvee.attached_energy
    item = evolvee.item
    turns = evolvee.turns_in_play
    damage_taken = evolvee.hp - evolvee.current_hp  # how much damage was taken
    
    # place new instance
    new_instance = PokemonInstance(evolver_card)
    new_instance.attached_energy = energy
    new_instance.item = item
    new_instance.turns_in_play = turns
    new_instance.current_hp -= damage_taken  # carry over damage
    
    if location == 0:
        state.current_player.active = new_instance
    else:
        state.current_player.bench[location - 1] = new_instance
    damage_taken = evolvee.hp - evolvee.current_hp
    
    new_instance = PokemonInstance(evolver_card)
    new_instance.attached_energy = evolvee.attached_energy
    new_instance.item = evolvee.item
    new_instance.turns_in_play = evolvee.turns_in_play
    new_instance.current_hp = new_instance.hp - damage_taken
    
    new_instance.evolved_this_turn = True
    
    if location == 0:
        player.active = new_instance
    else:
        player.bench[location - 1] = new_instance

    return True 
    
   

def attack(state,index=0):
    ## TODO check pokemon energy before attacking
    ## TODO change pokemon saving to save as energy code instead of energy name
    atk = state.current_player.active.attacks[index]
    cost = atk['cost']
    # cost should look like htis ['{G}', '{C}']
    energy = state.current_player.active.attached_energy
    if not check_requirements(cost,energy):
        print("Lacking energy to attack!")
        return False
    
    
    damage = int(state.current_player.active.attacks[index]['damage'])
    damage_type = state.current_player.active.types[0]
    state.opponent.active.take_damage(damage, damage_type)
    print(f"DEBUG attack: current={state.current_player.deck_name}, opponent={state.opponent.deck_name}")
    print(f"DEBUG: attacking {state.opponent.active.name}")
    check_knockout(state)
    state.pass_turn()

def ability(state, location):
    pokemon = get_location(state, location)
    
    if not pokemon:
        print("No Pokemon at this location!")
        return False
        
    if not pokemon.abilities:
        print("This Pokemon has no abilities!")
        return False

    if getattr(pokemon, 'ability_used', False): 
        print(f"{pokemon.name} has already used its ability this turn!")
        return False
        
    ability_data = pokemon.abilities[0]
    
    if "effect_id" in ability_data and ability_data["effect_id"]:
        resolve_effects(state, ability_data["effect_id"], source=pokemon)
        
        pokemon.ability_used = True  
        
        return True
        
    return False

def use_ability():
    pass

def use_trainer():
    pass

def use_tool():
    pass

def retreat(state, replacement_index):
    active = state.current_player.active
    replacement = state.current_player.bench[replacement_index - 1]
    
    if replacement is None:
        print("No pokemon in that bench spot!")
        return
    
    if len(active.attached_energy) < active.retreat_cost:
        print(f"Not enough energy to retreat! Need {active.retreat_cost}, have {len(active.attached_energy)}")
        return
    
    for _ in range(active.retreat_cost):
        active.attached_energy.pop()
    
    state.current_player.active = replacement
    state.current_player.bench[replacement_index - 1] = active

    return True ## TODO do this for other actions


def end_turn(state):
    state.pass_turn()
    
    
# game loop stuff, here to prevent circualr imports because checking here stops errors
# TODO think about if this is the right choice
def check_win(state):
    if state.current_player.pts >= 3:
        print(f"{state.current_player.deck_name} wins!")
        return True
    if state.opponent.pts >= 3:
        print(f"{state.opponent.deck_name} wins!")  # was current_player
        return True
    return False


def check_knockout(state):
    if state.opponent.active is None:
        return
    if state.opponent.active.current_hp <= 0:
        available_bench = [p for p in state.opponent.bench if p is not None]
        pts = points_on_knockout(state.opponent.active, bool(available_bench))
        state.current_player.add_pts(pts)
        print(f"{state.opponent.active.name} was knocked out! +{pts} point(s)")
        state.opponent.active = None
        # removed auto send 
            
def points_on_knockout(pokemon, has_bench):
    name = pokemon.name.lower()
    if not has_bench:
        return 3  # instant win bonus
    if "ex" in name:
        return 2
    elif "mega" in name:
        return 3
    else:
        return 1