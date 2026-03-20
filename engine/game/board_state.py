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
        
    def __repr__(self):
        return (
            f"\n=== TURN {self.turn} | {self.current_player.deck_name}'s TURN ===\n"
            f"\n[YOU - {self.current_player.deck_name} | PTS: {self.current_player.pts}]\n"
            f"Active:  {self.current_player.active}\n"
            f"Bench:   {self.current_player.bench}\n"
            f"Hand:    {len(self.current_player.hand)} cards\n"
            f"\n[OPPONENT - {self.opponent.deck_name} | PTS: {self.opponent.pts}]\n"
            f"Active:  {self.opponent.active}\n"
            f"Bench:   {self.opponent.bench}\n"
            f"Hand:    {len(self.opponent.hand)} cards\n"
            f"\n{'='*30}\n"
        )
        
        
    def pass_turn(self):
        self.turn += 1
        self.current_player, self.opponent = self.opponent, self.current_player
        self.current_player.draw_card()