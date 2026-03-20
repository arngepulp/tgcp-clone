# game/battle.py
from engine.game.actions import play_pokemon, attach_energy, attack, retreat

def run_loop(state):
    while True:
        if state.opponent.active is None:  # guard before attacking
            break
        attack(state)
        check_knockout(state)
        if check_win(state):
            break

def check_knockout(state):
    if state.opponent.active is None:
        return

    if state.opponent.active.current_hp <= 0:
        pts = points_on_knockout(state.opponent.active)
        state.current_player.add_pts(pts)
        print(f"{state.opponent.active.name} was knocked out! +{pts} point(s)")
        state.opponent.active = None

        available_bench = [p for p in state.opponent.bench if p is not None]

        if not available_bench:
            return  # let check_win handle it

        for i, p in enumerate(state.opponent.bench):
            if p is not None:
                state.opponent.active = p
                state.opponent.bench[i] = None
                print(f"{state.opponent.deck_name} sends out {state.opponent.active.name}!")
                break
            
def points_on_knockout(pokemon):
    name = pokemon.name.lower()
    if "ex" in name:
        return 2
    elif "mega" in name:
        return 3
    else:
        return 1
    
def check_win(state):
    if state.current_player.pts >= 3:
        print(f"{state.current_player.deck_name} wins!")
        return True
    if state.opponent.pts >= 3:
        print(f"{state.opponent.deck_name} wins!")  # was current_player
        return True
    return False