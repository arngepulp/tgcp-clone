# tests/test_actions.py
from engine.models.player import Player
from engine.game.board_state import Gamestate
from engine.game.actions import play_pokemon, attach_energy, attack, end_turn, retreat, check_requirements
from engine.models.card import load_card
from engine.models.pokemon import PokemonInstance

def setup_game():
    p1 = Player("bulb")
    p2 = Player("ponyta")
    game = Gamestate(p1, p2)
    game.player1.hand = ["A1-001"]
    game.player2.hand = ["A1-042"]
    return game

def test_play_pokemon_active():
    game = setup_game()
    card_id = game.current_player.hand[0]
    play_pokemon(game, card_id, 0)
    assert game.current_player.active is not None


def test_play_pokemon_removes_from_hand():
    game = setup_game()
    card_id = game.current_player.hand[0]
    play_pokemon(game, card_id, 0)
    assert card_id not in game.current_player.hand

def test_attach_energy():
    game = setup_game()
    game.first_turn = False  # bypass first turn rule
    play_pokemon(game, game.current_player.hand[0], 0)
    attach_energy(game, location=0)
    assert "{G}" in game.current_player.active.attached_energy

def test_attack_deals_damage():
    game = setup_game()
    ponyta = PokemonInstance(load_card("A1-042"))
    bulbasaur = PokemonInstance(load_card("A1-001"))
    game.current_player.active = ponyta
    game.opponent.active = bulbasaur
    ponyta.attached_energy = ["{R}"]  # give enough energy to attack
    target = game.opponent.active
    hp_before = target.current_hp
    attack(game)
    assert target.current_hp < hp_before

def test_end_turn_swaps_player():
    game = setup_game()
    p1 = game.current_player
    end_turn(game)
    assert game.current_player != p1
    
def test_retreat():
    game = setup_game()
    
    # manually place pokemon
    active = PokemonInstance(load_card("A1-001"))    # bulbasaur
    benched = PokemonInstance(load_card("A1-042"))   # ponyta
    
    game.current_player.active = active
    game.current_player.bench[0] = benched
    
    # give enough energy to retreat (bulbasaur retreat cost is 1)
    active.attached_energy = ["{C}"]
    
    retreat(game, 1)
    
    # ponyta should now be active
    assert game.current_player.active.name == "Ponyta"
    # bulbasaur should now be on bench
    assert game.current_player.bench[0].name == "Bulbasaur"
    # energy should be discarded
    assert len(game.current_player.active.attached_energy) == 0
    
    
    def test_check_requirements():
        assert check_requirements(['{G}', '{C}'], ['{G}', '{G}']) == True  # extra G covers colorless
        assert check_requirements(['{G}', '{C}'], ['{G}']) == False  # not enough
        assert check_requirements(['{G}', '{G}'], ['{G}', '{R}']) == False  # wrong type
        assert check_requirements(['{C}', '{C}'], ['{G}', '{R}']) == True  # any 2 covers colorless