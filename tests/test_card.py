# tests/test_card.py
from engine.models.card import load_card, PokemonCard

def test_load_card_returns_pokemon_card():
    card = load_card("A1-001")
    assert isinstance(card, PokemonCard)

def test_card_name():
    card = load_card("A1-001")
    assert card.name == "Bulbasaur"

def test_card_hp():
    card = load_card("A1-001")
    assert card.hp == 70

def test_card_types():
    card = load_card("A1-001")
    assert card.types == ["Grass"]

def test_card_stage():
    card = load_card("A1-001")
    assert card.stage == 0