from engine.models.card import load_card, PokemonCard
from engine.models.pokemon import PokemonInstance
from collections import Counter

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

def get_location(state,location):
    # checks if a pokemon is in a location, if it is returns the pokemon instnace
    # returns None if else
    if location == 0:
        return state.current_player.active  # None if empty
    else:
        return state.current_player.bench[location - 1]  # None if empty
    

def play_pokemon(state, card_id, location):
    if get_location(state, location) is not None:
        print("That spot is already taken!")
        return
    
    card = load_card(card_id)
    pokemon = PokemonInstance(card)
    
    
    if pokemon.evolves_from is not None:
        print("this is not a basic pokemon!")
        return
    
    if location == 0:
        state.current_player.active = pokemon
    else:
        state.current_player.bench[location - 1] = pokemon
    
    # remove from hand
    if card_id in state.current_player.hand:
        state.current_player.hand.remove(card_id)
   

    
def attach_energy(state,location=0):
    if state.first_turn:
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
    
def evolve_pokemon(state,location,evolver_id):
    # check if pokemon has been out for at least 1 turn
    evolvee = get_location(state,location)
    if evolvee is None:
        print("No pokemon in that spot!")
        return
    
    if evolvee.turns_in_play < 1:
        print("This pokemon has not been out long enough")
        return
    # check if proper evolves from
    
    evolver_card = load_card(evolver_id)  # load from json
    if evolver_card.evolves_from != evolvee.name:
        print("This pokemon does not evolve from that pokemon!")
        return
    
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
    check_knockout(state)
    state.pass_turn()



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