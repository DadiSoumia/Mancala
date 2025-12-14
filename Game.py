from MancalaBoard import MancalaBoard

class Game:
    def __init__(self, humanPlayer=1, computerPlayer=2):
        self.state = MancalaBoard()
        self.playerSide = {
            "HUMAN": humanPlayer,
            "COMPUTER": computerPlayer
        }

    def gameOver(self):
        """
        Vérifie si la partie est terminée.
        Si un joueur n’a plus de graines, ramasse toutes celles de l’autre joueur
        et les place dans son store.
        """

        board = self.state.board

        # Vérifier si tous les pits de player1 ou player2 sont vides
        player1_empty = all(board[p] == 0 for p in self.state.player1_pits)
        player2_empty = all(board[p] == 0 for p in self.state.player2_pits)

        # Si aucun côté n'est vide, la partie continue
        if not (player1_empty or player2_empty):
            return False

        # Ramasser les graines restantes
        if player1_empty:
            for p in self.state.player2_pits:
                board['Store2'] += board[p]
                board[p] = 0
        elif player2_empty:
            for p in self.state.player1_pits:
                board['Store1'] += board[p]
                board[p] = 0

        return True
   
    def findWinner(self):
        """
        Retourne le gagnant de la partie et les scores.
        """
        store1 = self.state.board['Store1']
        store2 = self.state.board['Store2']

        if store1 > store2:
            return "Player 1 wins", store1, store2
        elif store2 > store1:
            return "Player 2 wins", store1, store2
        else:
            return "Draw", store1, store2
        
        
    def evaluate(self):
       """
        Évalue le plateau actuel pour l'IA.
        Valeur positive = avantage ordinateur
        Valeur négative = avantage humain
       """
       board = self.state.board

       # Déterminer quel store correspond à l'ordinateur et à l'humain
       if self.playerSide["COMPUTER"] == 1:
          computer_store = board['Store1']
       else:
          computer_store = board['Store2']

       if self.playerSide["HUMAN"] == 1:
          human_store = board['Store1']
       else:
         human_store = board['Store2']

       # Calcul de la valeur du plateau
       value = computer_store - human_store

       return value