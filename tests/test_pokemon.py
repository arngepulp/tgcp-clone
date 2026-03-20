# tests/test_pokemon.py
from engine.models.card import load_card
from engine.models.pokemon import PokemonInstance

def test_take_damage():
    card = load_card("A1-001")
    pokemon = PokemonInstance(card)
    pokemon.take_damage(20, "Fire")
    assert pokemon.current_hp == 50

def test_attach_energy():
    card = load_card("A1-001")
    pokemon = PokemonInstance(card)
    pokemon.attach_energy("{G}")
    assert pokemon.attached_energy == ["{G}"]