class Gamestate():
    def __init__(self,player1,player2):
        
        self.player1 = player1
        self.player2 = player2
        self.turn = 1
        self.current_player = player1
        self.opponent = player2
        self.first_turn = True
        self.phase = 'setup'

        
        
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
        finished_player = self.current_player
        
        self.first_turn = False
        all_pokemon = [finished_player.active] + [p for p in finished_player.bench if p]
        
        for pkmn in all_pokemon:
            if pkmn:
                pkmn.turns_in_play += 1
                pkmn.ability_used = False      # Reset for their next turn
                pkmn.evolved_this_turn = False  # Reset evolution restriction
                
        finished_player.energy_attached_this_turn = False

       
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.opponent = self.player1
        else:
            self.current_player = self.player1
            self.opponent = self.player2
            
        if hasattr(self.current_player, 'deck') and len(self.current_player.deck) > 0:
            new_card = self.current_player.deck.pop(0)
            self.current_player.hand.append(new_card)
            print(f"DEBUG: New player drew {new_card}")
        else:
            print("DEBUG: Deck is empty, cannot draw!")
                
