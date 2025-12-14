from Game import Game

class play : 
    
    def __init__(self):
        self.game = Game() 
        

    def humanTurn(self):
        # Étape A : afficher le plateau
        board = self.game.state.board
        print("\nPlateau actuel :")
        print(board)

        # Étape B : obtenir les coups possibles
        human = self.game.playerSide["HUMAN"]
        moves = self.game.state.possibleMoves(human)
        if not moves:
            print("Aucun coup possible pour vous !")
            return

        # Étape C : demander à l'humain de choisir un pit valide
        pit = input(f"Choisissez un pit parmi {moves} : ").upper()
        while pit not in moves:
            pit = input(f"Coup invalide. Choisissez un pit parmi {moves} : ").upper()

        # Étape D : appliquer le coup
        self.game.state.doMove(human, pit)


    def computerTurn(self, depth=5):
        print("\n--- Tour de l'ordinateur ---")
        board = self.game.state.board
        print("Plateau actuel :")
        print(board)
        computer = self.game.playerSide["COMPUTER"]

        # Appel Minimax + Alpha-Beta
        value, bestPit = self.MinimaxAlphaBetaPruning(
           self.game,
           player=1,  # MAX = ordinateur
           depth=depth,
           alpha=-float('inf'),
           beta=float('inf')
        )

        print(f"L'ordinateur choisit le pit : {bestPit}")

        # Jouer le coup
        self.game.state.doMove(computer, bestPit)
 