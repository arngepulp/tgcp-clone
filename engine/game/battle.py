# game/battle.py
from engine.game.actions import play_pokemon, attach_energy, attack, retreat
from interfaces.cli import choose_action

def setup_phase(state):
    from engine.models.card import load_card
    
    for player in [state.player1, state.player2]:
        state.current_player = player
        state.opponent = state.player2 if player == state.player1 else state.player1
        
        print(f"\n{player.deck_name} - place your starting active pokemon")
        
        # show hand with names
        print("Your hand:")
        for i, card_id in enumerate(player.hand):
            card = load_card(card_id)
            print(f"  [{i}] {card.name} ({card_id})")
        
        # must place an active first
        while state.current_player.active is None:
            choice = int(input("Choose active (must be basic): "))
            card_id = player.hand[choice]
            play_pokemon(state, card_id, 0)
        
        # optionally fill bench
        while True:
            print("\nBench:", player.bench)
            print("Your hand:")
            for i, card_id in enumerate(player.hand):
                card = load_card(card_id)
                print(f"  [{i}] {card.name} ({card_id})")
            
            choice = input("Place to bench? (index or 's' to skip): ")
            if choice == "s":
                break
            
            card_id = player.hand[int(choice)]
            bench_slot = int(input("Bench slot (1-3): "))
            play_pokemon(state, card_id, bench_slot)
    
    state.current_player = state.player1
    state.opponent = state.player2

def run_loop(state):
    while True:
        if state.opponent.active is None and not any(state.opponent.bench):
            break
        choose_action(state)
        if check_win(state):
            break


            

    
