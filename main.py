# main.py
from engine.models.player import Player
from engine.game.board_state import Gamestate
from engine.game.battle import run_loop
from engine.game.actions import play_pokemon
from engine.game.actions import play_pokemon, end_turn

p1 = Player("bulb")
p2 = Player("ponyta")
game = Gamestate(p1, p2)

# place starting pokemon
play_pokemon(game, game.current_player.hand[0], 0)
end_turn(game)
play_pokemon(game, game.current_player.hand[0], 0)
end_turn(game)

run_loop(game)