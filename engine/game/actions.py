from engine.models.card import load_card, PokemonCard
from engine.models.pokemon import PokemonInstance

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
    instance = get_location(state, location)
    if instance is None:
        print("No pokemon in that spot!")
        return
    instance.attach_energy(state.current_player.energy_pool[0])
    state.current_player.energy_draw()
    
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
    damage = int(state.current_player.active.attacks[index]['damage'])
    damage_type = state.current_player.active.types[0]
    state.opponent.active.take_damage(damage, damage_type)
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
    

