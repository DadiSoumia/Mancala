class MancalaBoard:
    def __init__(self):

        self.board = {
                'A': 4, 'B': 4, 'C': 4,'D': 4, 'E': 4, 'F': 4,
                'G': 4, 'H': 4, 'I': 4,'J': 4, 'K': 4, 'L': 4, 
                'Store1': 0, 'Store2': 0
                     }
   
        self.player1_pits = ('A', 'B', 'C', 'D', 'E', 'F')
        self.player2_pits = ('G', 'H', 'I', 'J', 'K', 'L')

        self.opposite = {
                'A':'G', 'B':'H', 'C':'I', 'D':'J', 'E':'K', 'F':'L',
                'G':'A', 'H':'B', 'I':'C', 'J':'D', 'K':'E', 'L':'F'    
                        }
        
        self.next_pit = {
               
                'A':'B', 'B':'C', 'C':'D', 'D':'E', 'E':'F',
                'F':'Store1',
                'Store1':'L',
                'L':'K', 'K':'J', 'J':'I', 'I':'H', 'H':'G',
                'G':'Store2',
                'Store2':'A'
                       }
        
       

    def possibleMoves(self, player):
     
        if player == 1:
            pits = self.player1_pits
        else:
            pits = self.player2_pits
        
        moves = [pit for pit in pits if self.board[pit] > 0]
        
        return moves
    
    def doMove(self, player, pit):
        """
        Effectue un coup.
        
        Args:
            player: 1 ou 2
            pit: lettre du pit à jouer
        """
        if self.board[pit] == 0:
            print("Coup invalide : pit vide")
            return

        seeds = self.board[pit]
        self.board[pit] = 0
        current = pit

        while seeds > 0:
            current = self.next_pit[current]

            # Ignorer le store adverse
            if player == 1 and current == 'Store2':
                current = self.next_pit[current]
            elif player == 2 and current == 'Store1':
                current = self.next_pit[current]

            self.board[current] += 1
            seeds -= 1

        # Règle de capture
        player_pits = self.player1_pits if player == 1 else self.player2_pits
        store = 'Store1' if player == 1 else 'Store2'

        if current in player_pits and self.board[current] == 1:
            opp = self.opposite[current]
            if self.board[opp] > 0:  # Capture seulement si pit opposé non vide
                self.board[store] += 1 + self.board[opp]
                self.board[current] = 0
                self.board[opp] = 0


