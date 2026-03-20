# tests/test_actions.py
from engine.models.player import Player
from engine.game.board_state import Gamestate
from engine.game.actions import play_pokemon, attach_energy, attack, end_turn
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
    play_pokemon(game, game.current_player.hand[0], 0)
    attach_energy(game, "{G}", location=0)
    assert "{G}" in game.current_player.active.attached_energy

def test_attack_deals_damage():
    game = setup_game()
    
    bulbasaur = PokemonInstance(load_card("A1-001"))
    ponyta = PokemonInstance(load_card("A1-042"))
    
    # ponyta attacks bulbasaur
    game.current_player.active = ponyta
    game.opponent.active = bulbasaur
    
    target = game.opponent.active 
    hp_before = target.current_hp
    attack(game)
    assert target.current_hp < hp_before

def test_end_turn_swaps_player():
    game = setup_game()
    p1 = game.current_player
    end_turn(game)
    assert game.current_player != p1