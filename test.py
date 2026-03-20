from engine.models.card import load_card
from engine.models.pokemon import PokemonInstance
from engine.models.player import Player
from engine.game.board_state import Gamestate
from engine.game.battle import run_loop

p1 = Player("bulb")
p2 = Player("ponyta")
game = Gamestate(p1, p2)

# manually place pokemon with low hp so knockouts happen fast
bulbasaur = PokemonInstance(load_card("A1-001"))
ponyta = PokemonInstance(load_card("A1-042"))

bulbasaur.current_hp = 20   # will die in one hit
ponyta.current_hp = 20      # will die in one hit

game.player1.active = bulbasaur
game.player2.active = ponyta

run_loop(game)