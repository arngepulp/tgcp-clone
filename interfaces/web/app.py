# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file
from engine.game.actions import play_pokemon, attach_energy, attack, retreat, evolve_pokemon
from engine.game.battle import check_win
from engine.models.card import load_card, PokemonCard
from engine.models.player import Player
from engine.game.board_state import Gamestate
from engine.models.pokemon import PokemonInstance
from engine.game.battle import setup_phase
import os


p1 = Player("bulb")
p2 = Player("ponyta")
game = Gamestate(p1, p2)

game.player1.active = PokemonInstance(load_card("A1-001"))
game.player2.active = PokemonInstance(load_card("A1-042"))


app = Flask(__name__)


@app.route('/player1')
def player1():
    return render_template('game.html', player=game.player1, opponent=game.player2)

@app.route('/player2')  
def player2():
    return render_template('game.html', player=game.player2, opponent=game.player1)

@app.route('/setup/place_active', methods=['POST'])
def setup_place_active():
    choice = int(request.form['choice'])
    card_id = game.current_player.hand[choice]
    play_pokemon(game, card_id, 0)
    return redirect(url_for('setup_bench'))

@app.route('/setup/place_bench', methods=['POST'])
def setup_place_bench():
    choice = request.form.get('choice')
    if choice == '-1':  # skip/done
        # swap to next player or start game
        return redirect(url_for('player1'))
    card_id = game.current_player.hand[int(choice)]
    bench_slot = int(request.form['bench_slot'])
    play_pokemon(game, card_id, bench_slot)
    return redirect(url_for('setup_bench'))  # come back to bench page to place more

@app.route('/attack', methods=['POST'])
def attack_route():
    index = int(request.form['attack_index'])
    attack(game,index)
    return redirect(url_for('player1'))

@app.route('/play_pokemon', methods=['POST'])
def play_pokemon_route():
    card_index = int(request.form['card_index'])
    location = int(request.form['location'])
    card_id = game.current_player.hand[card_index]
    play_pokemon(game, card_id, location)
    return redirect(url_for('player1'))

@app.route('/evolve', methods=['POST'])
def evolve_route():
    evolvable = []
    if game.current_player.active and game.current_player.active.turns_in_play >= 1:
        evolvable.append((0, game.current_player.active))
    for i, p in enumerate(game.current_player.bench):
        if p and p.turns_in_play >= 1:
            evolvable.append((i + 1, p))
    
    if not evolvable:
        return redirect(url_for('player1'))  # nothing to evolve
    
    board_names = [p.name for _, p in evolvable]
    valid_evolvers = []
    for card_id in game.current_player.hand:
        card = load_card(card_id)
        if card.evolves_from in board_names:
            valid_evolvers.append(card_id)
    
    if not valid_evolvers:
        return redirect(url_for('player1'))  # no evolvers in hand
    
    evolver_id = valid_evolvers[int(request.form['evolver_index'])]
    evolver_card = load_card(evolver_id)
    targets = [(loc, p) for loc, p in evolvable if p.name == evolver_card.evolves_from]
    
    if len(targets) == 1:
        location = targets[0][0]
    else:
        location = targets[int(request.form['location'])][0]
    
    evolve_pokemon(game, location, evolver_id)
    return redirect(url_for('player1'))

@app.route('/attach_energy', methods=['POST'])
def attach_energy_route():
    location = int(request.form['location'])
    attach_energy(game, location)
    return redirect(url_for('player1'))

@app.route('/retreat', methods=['POST'])
def retreat_route():
    index = int(request.form['bench_index'])
    retreat(game, index)
    return redirect(url_for('player1'))

@app.route('/end_turn', methods=['POST'])
def end_turn_route():
    from engine.game.actions import end_turn
    end_turn(game)
    return redirect(url_for('player1'))

@app.route('/card_image/<card_type>/<collection_id>/<card_id>')
def card_image(card_type, collection_id, card_id):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(root, 'data', 'cards', card_type, collection_id, 'image', f'{card_id}.png')
    return send_file(path, mimetype='image/png')

app.run()