from engine.models.card import load_card
from engine.models.pokemon import PokemonInstance
from engine.models.player import Player
from engine.game.board_state import Gamestate
from engine.game.actions import *

# can i load a card
# cards.py
card = load_card("A1-001")
print(card.name, card.hp)

# can i make it a pokemon
#pokemon.py
pokemon = PokemonInstance(card)
print(pokemon.current_hp, pokemon.turns_in_play)

# can i make a player
p1 = Player("bulb")
print(p1.deck)

# can i put  them on the board
p2 = Player("ponyta")
game = Gamestate(p1,p2)

# can i place a mon
# check if has hand
print(game.current_player.hand)
play_pokemon(game,game.current_player.hand[0] ,0)
print(game.current_player.active)

# can i add energy
attach_energy(game,"{G}", location=0)
print(game.current_player.active)

# next players turn?
print(game.opponent.hand)
end_turn(game)
print(game.opponent.hand)

play_pokemon(game,game.current_player.hand[0] ,0)
print(game.current_player)

# print pokemons attacks
print(game.current_player.active.attacks[0]['damage'])
print(game.opponent.active.current_hp)
attack(game)
print(game.current_player.active.current_hp)


# clear