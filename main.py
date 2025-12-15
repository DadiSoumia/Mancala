from Game import Game
from Play import Play

def display_board(game):
    """Affiche le plateau de manière lisible"""
    board = game.state.board
    print("\n" + "="*50)
    print(f"      G    H    I    J    K    L")
    print(f"   +----+----+----+----+----+----+")
    print(f"   | {board['L']:2} | {board['K']:2} | {board['J']:2} | {board['I']:2} | {board['H']:2} | {board['G']:2} |")
    print(f"   +----+----+----+----+----+----+")
    print(f"{board['Store2']:2} |                            | {board['Store1']:2}")
    print(f"   +----+----+----+----+----+----+")
    print(f"   | {board['A']:2} | {board['B']:2} | {board['C']:2} | {board['D']:2} | {board['E']:2} | {board['F']:2} |")
    print(f"   +----+----+----+----+----+----+")
    print(f"      A    B    C    D    E    F")
    print("="*50 + "\n")

def main():
    print("=== Bienvenue au jeu de Mancala ===")
    print("Vous êtes le joueur 1 (pits A-F)")
    print("L'ordinateur est le joueur 2 (pits G-L)\n")
    
    # Créer le jeu
    game = Game(humanPlayer=1, computerPlayer=2)
    play = Play(game)
    
    display_board(game)
    
    current_player = "HUMAN"  # L'humain commence
    
    while not game.gameOver():
        if current_player == "HUMAN":
            print("\n>>> VOTRE TOUR <<<")
            play.humanTurn()
            display_board(game)
            current_player = "COMPUTER"
        else:
            print("\n>>> TOUR DE L'ORDINATEUR <<<")
            play.computerTurn(depth=6)
            display_board(game)
            current_player = "HUMAN"
    
    # Afficher le résultat
    print("\n" + "="*50)
    print("PARTIE TERMINÉE !")
    result, score1, score2 = game.findWinner()
    print(f"\n{result}")
    print(f"Score Player 1 (Vous): {score1}")
    print(f"Score Player 2 (Ordinateur): {score2}")
    print("="*50)

if __name__ == "__main__":
    main()