class Gamestate():
    def __init__(self,player1,player2):
        
        self.player1 = player1
        self.player2 = player2
        self.turn = 1
        self.current_player = player1
        self.opponent = player2
        
        # and proper hand drawing behavior later
        self.player1.draw_card()
        self.player2.draw_card()
        
    def pass_turn(self):
        self.turn += 1
        self.current_player, self.opponent = self.opponent, self.current_player
        self.current_player.draw_card()