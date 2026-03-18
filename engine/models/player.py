import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from engine.rules.game_rules import PTS_TO_WIN

class Player:
    def __init__(self):
        self.pts = 0
        
        #board
        self.active = None
        self.bench = [None, None, None]
        
        self.deck = []
        self.hand = []
        self.discard = []
        
        self.attached_energy = False
        self.has_attacked = False
        
        
        
    def add_pts(self, n):
        self.pts += n
        if self.pts >= PTS_TO_WIN:
            # TODO win game
            pass