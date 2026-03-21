# tests/test_player.py
from engine.models.player import Player

def test_player_deck_loads():
    p = Player("bulb")
    assert len(p.deck) > 0

def test_player_draw_card():
    p = Player("bulb")
    deck_size = len(p.deck)
    p.draw_card()
    assert len(p.hand) == 5+1 ## TODO add this as a rule to consts, add in player draw card func aswell
    assert len(p.deck) == deck_size - 1

def test_player_add_pts():
    p = Player("bulb")
    p.add_pts(1)
    assert p.pts == 1

def test_player_active_starts_none():
    p = Player("bulb")
    assert p.active is None

def test_player_bench_starts_empty():
    p = Player("bulb")
    assert p.bench == [None, None, None]