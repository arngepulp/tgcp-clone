# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_socketio import SocketIO
from engine.game.actions import play_pokemon, attach_energy, attack, retreat, evolve_pokemon, end_turn, check_win, ability
from engine.models.card import load_card, PokemonCard
from engine.models.player import Player
from engine.game.board_state import Gamestate
from engine.models.pokemon import PokemonInstance
import os
from consts import ENERGY_SYMBOLS


p1 = Player("bulb")
p2 = Player("ponyta")
game = Gamestate(p1, p2)


app = Flask(__name__)
app.secret_key = 'tgcp-secret'
socketio = SocketIO(app)

player_sockets = {}  # track which socket belongs to which player

@socketio.on('register')
def handle_register(data):
    player_sockets[data['player']] = request.sid
    print(f"DEBUG: player {data['player']} registered with socket {request.sid}")

def redirect_or_win(player_num):
    # Just check for a winner, then tell BOTH browsers to refresh and stay on the game page.
    if check_win(game):
        socketio.emit('refresh', {})
        return redirect(url_for('winner'))
    
    socketio.emit('refresh', {})
    return redirect(url_for(f'player{player_num}'))

# Add this new route to handle promoting a benched pokemon
@app.route('/promote', methods=['POST'])
def promote_route():
    player_num = request.form['player']
    
    # Ensure it's the correct player's turn
    if (player_num == '1' and game.current_player != game.player1) or \
       (player_num == '2' and game.current_player != game.player2):
        flash("It's not your turn!")
        return redirect(url_for(f'player{player_num}'))
    
    bench_index = int(request.form['bench_index'])
    current_p = game.player1 if player_num == '1' else game.player2
    
    # Move the chosen pokemon to active and clear that bench spot
    if current_p.active is None and current_p.bench[bench_index] is not None:
        current_p.active = current_p.bench[bench_index]
        current_p.bench[bench_index] = None
    else:
        flash("Cannot promote this Pokémon.")
        
    return redirect_or_win(player_num)

@app.route('/')
def index():
    return redirect(url_for('player1'))

@app.route('/player1')
def player1():
    # ADDED ENERGY_SYMBOLS HERE
    return render_template('game.html', player=game.player1, opponent=game.player2, player_num=1, game=game, ENERGY_SYMBOLS=ENERGY_SYMBOLS)

@app.route('/player2')
def player2():
    # ADDED ENERGY_SYMBOLS HERE
    return render_template('game.html', player=game.player2, opponent=game.player1, player_num=2, game=game, ENERGY_SYMBOLS=ENERGY_SYMBOLS)

@app.route('/winner')
def winner():
    return render_template('winner.html', winner=game.current_player.deck_name)

@app.route('/attack', methods=['POST'])
def attack_route():
    player_num = request.form['player']
    if (player_num == '1' and game.current_player != game.player1) or \
       (player_num == '2' and game.current_player != game.player2):
        flash("It's not your turn!")
        return redirect(url_for(f'player{player_num}'))
    index = int(request.form['attack_index'])
    result = attack(game, index)
    if result == False:
        flash("Not enough energy to attack!")
        return redirect(url_for(f'player{player_num}'))
    return redirect_or_win(player_num)

@app.route('/use_ability', methods=['POST'])
def use_ability_route():
    player_num = request.form['player']
    
    # 1. Check if it's the correct player's turn
    if (player_num == '1' and game.current_player != game.player1) or \
       (player_num == '2' and game.current_player != game.player2):
        flash("It's not your turn!")
        return redirect(url_for(f'player{player_num}'))
    
    # 2. Grab the location and trigger the engine function
    location = int(request.form['location'])
    result = ability(game, location)
    
    # 3. Handle failures or refresh the page
    if result == False:
        flash("Cannot use ability! (No Pokémon there, or no ability available)")
        return redirect(url_for(f'player{player_num}'))
        
    return redirect_or_win(player_num)

@app.route('/play_or_evolve', methods=['POST'])
def play_or_evolve_route():
    player_num = request.form['player']
    if (player_num == '1' and game.current_player != game.player1) or \
       (player_num == '2' and game.current_player != game.player2):
        flash("It's not your turn!")
        return redirect(url_for(f'player{player_num}'))
    card_index = int(request.form['card_index'])
    location = int(request.form['location'])
    card_id = game.current_player.hand[card_index]
    card = load_card(card_id)
    if card.evolves_from is not None:
        result = evolve_pokemon(game, location, card_id)
        if result == False:
            flash("Cannot evolve that pokemon!")
    else:
        result = play_pokemon(game, card_id, location)
        if result == False:
            flash("Cannot play pokemon there!")
    return redirect_or_win(player_num)

@app.route('/attach_energy', methods=['POST'])
def attach_energy_route():
    player_num = request.form['player']
    if (player_num == '1' and game.current_player != game.player1) or \
       (player_num == '2' and game.current_player != game.player2):
        flash("It's not your turn!")
        return redirect(url_for(f'player{player_num}'))
    location = int(request.form['location'])
    result = attach_energy(game, location)
    if result == False:
        flash("Cannot attach energy!")
    return redirect(url_for(f'player{player_num}'))

@app.route('/retreat', methods=['POST'])
def retreat_route():
    player_num = request.form['player']
    if (player_num == '1' and game.current_player != game.player1) or \
       (player_num == '2' and game.current_player != game.player2):
        flash("It's not your turn!")
        return redirect(url_for(f'player{player_num}'))
    index = int(request.form['bench_index'])
    result = retreat(game, index)
    if result == False:
        flash("Cannot retreat!")
    return redirect_or_win(player_num)

@app.route('/end_turn', methods=['POST'])
def end_turn_route():
    player_num = request.form['player']
    if (player_num == '1' and game.current_player != game.player1) or \
       (player_num == '2' and game.current_player != game.player2):
        flash("It's not your turn!")
        return redirect(url_for(f'player{player_num}'))
    end_turn(game)
    return redirect_or_win(player_num)

@app.route('/card_image/<card_type>/<collection_id>/<card_id>')
def card_image(card_type, collection_id, card_id):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(root, 'data', 'cards', card_type, collection_id, 'image', f'{card_id}.png')
    return send_file(path, mimetype='image/png')


@app.route('/send_out')
def send_out():
    if game.player1.active is None and any(p for p in game.player1.bench if p):
        knocked_player = game.player1
        knocked_num = 1
    else:
        knocked_player = game.player2
        knocked_num = 2
    print(f"DEBUG send_out: knocked_num={knocked_num}, bench={knocked_player.bench}")
    return render_template('send_out.html', player=knocked_player, player_num=knocked_num)


@app.route('/send_out/choose', methods=['POST'])
def send_out_choose():
    player_num = request.form['player']
    bench_index = int(request.form['bench_index'])
    knocked_player = game.player1 if player_num == '1' else game.player2
    knocked_player.active = knocked_player.bench[bench_index]
    knocked_player.bench[bench_index] = None
    socketio.emit('refresh', {})
    return redirect(url_for(f'player{player_num}'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)