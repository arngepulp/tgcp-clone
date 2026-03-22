# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_socketio import SocketIO
from engine.game.actions import play_pokemon, attach_energy, attack, retreat, evolve_pokemon, end_turn, check_win, ability, get_location
from engine.models.card import load_card, PokemonCard, load_all_cards, filter_cards
from engine.models.player import Player
from engine.game.board_state import Gamestate
from engine.models.pokemon import PokemonInstance
import os, json
from consts import ENERGY_SYMBOLS, SETS, RARITIES
from flask import jsonify


ALL_CARDS = load_all_cards()
current_deck = {"name": "", "energy": [], "cards": {}}

p1 = Player("bulb")
p2 = Player("ponyta")
game = Gamestate(p1, p2)
game.phase = 'setup' 



app = Flask(__name__)
app.secret_key = 'tgcp-secret'
socketio = SocketIO(app)

player_sockets = {}  # track which socket belongs to which player

@socketio.on('register')
def handle_register(data):
    player_sockets[data['player']] = request.sid
    print(f"DEBUG: player {data['player']} registered with socket {request.sid}")

def redirect_or_win(player_num):
    if check_win(game):
        socketio.emit('refresh', {})
        return redirect(url_for('winner'))
    
    socketio.emit('refresh', {})
    return redirect(url_for(f'player{player_num}'))


@app.route('/promote', methods=['POST'])
def promote_route():
    player_num = request.form['player']
    
    if (player_num == '1' and game.current_player != game.player1) or \
       (player_num == '2' and game.current_player != game.player2):
        flash("It's not your turn!")
        return redirect(url_for(f'player{player_num}'))
    
    bench_index = int(request.form['bench_index'])
    current_p = game.player1 if player_num == '1' else game.player2
    
    if current_p.active is None and current_p.bench[bench_index] is not None:
        current_p.active = current_p.bench[bench_index]
        current_p.bench[bench_index] = None
    else:
        flash("Cannot promote this Pokémon.")
        
    return redirect_or_win(player_num)

@app.route('/')
def index():
    return redirect(url_for('player1'))

@app.route('/finish_setup', methods=['POST'])
def finish_setup():
    player_num = int(request.form.get('player')) # This is 1 or 2
    player = game.player1 if player_num == 1 else game.player2

    player.ready = True

    if getattr(game.player1, 'ready', False) and getattr(game.player2, 'ready', False):
        game.phase = 'playing'
        game.current_player = game.player1 
        socketio.emit('refresh') 
        
    return redirect(url_for(f'player{player_num}'))

@app.route('/player1')
def player1():
    return render_template('game.html', player=game.player1, opponent=game.player2, player_num=1, game=game, ENERGY_SYMBOLS=ENERGY_SYMBOLS)

@app.route('/player2')
def player2():
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
    
   
    if (player_num == '1' and game.current_player != game.player1) or \
       (player_num == '2' and game.current_player != game.player2):
        flash("It's not your turn!")
        return redirect(url_for(f'player{player_num}'))
    

    location = int(request.form['location'])
    result = ability(game, location)
    
    if result == False:
        flash("Cannot use ability! (No Pokémon there, or no ability available)")
        return redirect(url_for(f'player{player_num}'))
        
    return redirect_or_win(player_num)


@app.route('/play_or_evolve', methods=['POST'])
def play_or_evolve():
    player_num = int(request.form.get('player'))
    card_index = int(request.form.get('card_index'))
    location_index = int(request.form.get('location'))
    
    player = game.player1 if player_num == 1 else game.player2
    card_id = player.hand[card_index]
    
    target = get_location(player, location_index)
    
    if target is not None:
        success = evolve_pokemon(game, location_index, card_id)
    else:
        success = play_pokemon(game, card_id, location_index, forced_player=player)

    if success:
        socketio.emit('refresh')
    
    return redirect(url_for(f'player{player_num}'))

@app.route('/attach_energy', methods=['POST'])
def attach_energy_route():
    player_num = request.form['player']
    
    if game.phase != 'setup':
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

@app.route('/card_image/<collection_id>/<card_id>')
def card_image(collection_id, card_id):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for card_type in ['pokemon', 'trainer']:
        path = os.path.join(root, 'data', 'cards', card_type, collection_id, 'image', f'{card_id}.png')
        if os.path.exists(path):
            return send_file(path, mimetype='image/png')
    return '', 404


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

## deck builder stuff
@app.route('/deckbuilder')
def deckbuilder():
    print(f"DEBUG: ALL_CARDS count = {len(ALL_CARDS)}")
    search = request.args.get('search', '')
    type_filter = request.args.get('type', '')
    min_hp = request.args.get('min_hp', 0, type=int)
    max_hp = request.args.get('max_hp', 999, type=int)
    has_ability = request.args.get('has_ability') == 'true'
    set_filter = request.args.get('set', '')
    is_ex = request.args.get('is_ex') == 'true'
    is_trainer = request.args.get('is_trainer') == 'true'
    rarity = request.args.get('rarity', '')
    
    filtered = filter_cards(ALL_CARDS, type_filter, min_hp, max_hp,
                            has_ability, set_filter, is_ex, is_trainer, search, rarity)
    
    saved_decks = [f.replace('.json', '') for f in os.listdir('decks') if f.endswith('.json')]
    
    return render_template('deckbuilder.html', 
                           cards=filtered,
                           current_deck=current_deck,
                           saved_decks=saved_decks,
                           SETS=SETS,
                           RARITIES=RARITIES)

@app.route('/deckbuilder/add', methods=['POST'])
def deck_add():
    card_id = request.form['card_id']
    count = current_deck['cards'].get(card_id, 0)
    if count < 2:
        current_deck['cards'][card_id] = count + 1
        return jsonify({'deck': current_deck})
    return jsonify({'error': 'Max 2 copies of any card!'})

@app.route('/deckbuilder/remove', methods=['POST'])
def deck_remove():
    card_id = request.form['card_id']
    if card_id in current_deck['cards']:
        current_deck['cards'][card_id] -= 1
        if current_deck['cards'][card_id] <= 0:
            del current_deck['cards'][card_id]
    return jsonify({'deck': current_deck})

@app.route('/deckbuilder/save', methods=['POST'])
def deck_save():
    name = request.form['name']
    energy = request.form.getlist('energy')
    if not name:
        flash("Deck needs a name!")
        return redirect(url_for('deckbuilder'))
    if not current_deck['cards']:
        flash("Deck is empty!")
        return redirect(url_for('deckbuilder'))
    
    deck_data = {
        "name": name,
        "energy": energy,
        "cards": [{"id": k, "count": v} for k, v in current_deck['cards'].items()]
    }
    with open(f"decks/{name}.json", 'w') as f:
        json.dump(deck_data, f, indent=2)
    
    flash(f"Deck '{name}' saved!")
    return redirect(url_for('deckbuilder'))

@app.route('/deckbuilder/load/<deck_name>')
def deck_load(deck_name):
    global current_deck
    with open(f"decks/{deck_name}.json") as f:
        data = json.load(f)
    current_deck['name'] = data['name']
    current_deck['energy'] = data.get('energy', [])
    current_deck['cards'] = {c['id']: c['count'] for c in data['cards']}
    return redirect(url_for('deckbuilder'))

@app.route('/deckbuilder/clear', methods=['POST'])
def deck_clear():
    global current_deck
    current_deck = {"name": "", "energy": [], "cards": {}}
    return redirect(url_for('deckbuilder'))

@app.route('/deckbuilder/deck_data')
def deck_data():
    from flask import jsonify
    return jsonify(current_deck)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)