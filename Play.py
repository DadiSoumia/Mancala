from Game import Game
import copy
import math

MAX = 1      # COMPUTER
MIN = -1     # HUMAN

class Play:
    def __init__(self, game):
        self.game = game

    # ---------- TOUR HUMAIN ----------
    def humanTurn(self):
        moves = self.game.state.possibleMoves(self.game.playerSide["HUMAN"])
        if not moves:
            print("Aucun coup possible pour l'humain.")
            return

        print(f"Coups possibles : {moves}")
        pit = input("Choisissez un pit : ").upper()
        while pit not in moves:
            pit = input("Coup invalide. Choisissez un pit valide : ").upper()

        # Effectuer le mouvement
        self.game.state.doMove(self.game.playerSide["HUMAN"], pit)

    # ---------- TOUR ORDINATEUR ----------
    def computerTurn(self, depth=5):
        moves = self.game.state.possibleMoves(self.game.playerSide["COMPUTER"])
        if not moves:
            print("Aucun coup possible pour l'ordinateur.")
            return

        value, pit = self.minimaxAlphaBeta(
            self.game, MAX, depth, -math.inf, math.inf
        )

        print(f"L'ordinateur choisit le pit {pit} (valeur = {value})")

        # Effectuer le mouvement
        self.game.state.doMove(self.game.playerSide["COMPUTER"], pit)

    # ---------- MINIMAX ALPHA-BETA ----------
    def minimaxAlphaBeta(self, game, player, depth, alpha, beta):
        # Condition d'arrêt
        if depth == 0 or game.gameOver():
            return game.evaluate(), None

        # --------- MAX = COMPUTER ---------
        if player == MAX:
            bestValue = -math.inf
            bestPit = None

            for pit in game.state.possibleMoves(game.playerSide["COMPUTER"]):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(game.playerSide["COMPUTER"], pit)

                value, _ = self.minimaxAlphaBeta(
                    child_game, MIN, depth-1, alpha, beta
                )

                if value > bestValue:
                    bestValue = value
                    bestPit = pit

                if bestValue >= beta:
                    break  # élagage β

                alpha = max(alpha, bestValue)

            return bestValue, bestPit

        # --------- MIN = HUMAN ---------
        else:
            bestValue = math.inf
            bestPit = None

            for pit in game.state.possibleMoves(game.playerSide["HUMAN"]):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(game.playerSide["HUMAN"], pit)

                value, _ = self.minimaxAlphaBeta(
                    child_game, MAX, depth-1, alpha, beta
                )

                if value < bestValue:
                    bestValue = value
                    bestPit = pit

                if bestValue <= alpha:
                    break  # élagage α

                beta = min(beta, bestValue)

            return bestValue, bestPit