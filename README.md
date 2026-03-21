# tgcp-clone

useful resources database
https://ptcgpocket.gg/cards/
https://tcgdex.dev/sdks/python


pip install tcgdex-sdk
pip install pytest

trainers and supports are saved badly, not a current issue tho
basic engine first

models/card.py — load your JSON into a card object
models/pokemon.py — wrap a card into a battle instance
models/player.py — give a player a deck, hand, bench, active
game/state.py — hold two players and track turn/phase
game/rules.py — validate actions against the state
game/actions.py — mutate the state when actions happen
game/battle.py — the loop that drives it all
cli/display.py — print the state so you can actually see it

i want to make decks numbers not strings
so A1-001
A1 is the first collection so
001001

the idea is deck holds IDs but then load on demand

TODOS
so my next todos

add effects speacial test parsing to cards
add trains abilities tools
gui
status conditions