import pygame
import copy
import math
from Game import Game
from Play import Play

pygame.init()

# ==================== CONFIGURATION ====================
WIDTH, HEIGHT = 900, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mancala - Pygame")

# Couleurs
WOOD = (205, 155, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SEED_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (150, 0, 150)]
SELECTED_COLOR = (255, 215, 0)  # Or - pit sélectionné
MODIFIED_COLOR = (100, 200, 100)  # Vert clair - pits modifiés
HIGHLIGHT_DURATION = 10000  # millisecondes (10 secondes)

# Tailles
pit_radius = 40
seed_radius = 8

# Positions des pits
# Player 1 (en bas) : A B C D E F (indices 0-5)
# Player 2 (en haut) : G H I J K L (indices 6-11)
pit_positions = [
    (170 + i*110, 280) for i in range(6)  # A-F (Player 1, bas)
] + [
    (170 + i*110, 120) for i in range(6)  # G-L (Player 2, haut)
]

# Stores (magasins)
store_positions = [(840, 200), (60, 200)]  # [Store1, Store2]

# Mapping pit → index
pit_to_index = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
    'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11
}
index_to_pit = {v: k for k, v in pit_to_index.items()}

# ==================== INITIALISATION DU JEU ====================
game = None
play = None
current_player = None

# Infos du dernier coup
last_computer_move = {"pit": None, "value": None}

# Animations et surbrillance
highlighted_pit = None
modified_pits = set()
highlight_start_time = 0
board_before_move = {}

# Délai entre tours
delay_after_human_move = False
delay_start_time = 0
DELAY_DURATION = 800

# Menu de configuration
game_started = False
human_side_choice = None  # "bottom" ou "top"

# ==================== FONCTIONS DE DESSIN ====================
def draw_pit(center, label, highlight_type=None):
    """Dessine un pit avec son label et éventuellement une surbrillance"""
    x, y = center
    
    # Choisir la couleur selon le type de surbrillance
    if highlight_type == "selected":
        color = SELECTED_COLOR
        border_width = 5
    elif highlight_type == "modified":
        color = MODIFIED_COLOR
        border_width = 4
    else:
        color = WOOD
        border_width = 3
    
    pygame.draw.circle(screen, color, (x, y), pit_radius)
    pygame.draw.circle(screen, BLACK, (x, y), pit_radius, border_width)
    
    # Label du pit
    font = pygame.font.SysFont(None, 24)
    text = font.render(label, True, BLACK)
    screen.blit(text, (x - text.get_width()//2, y + pit_radius + 5))


def draw_seeds(seed_count, cx, cy):
    """Dessine les graines dans un pit"""
    if seed_count == 0:
        return
    
    # Afficher le nombre de graines
    font = pygame.font.SysFont(None, 32, bold=True)
    text = font.render(str(seed_count), True, WHITE)
    screen.blit(text, (cx - text.get_width()//2, cy - text.get_height()//2))


def draw_store(i, is_modified=False):
    """Dessine un store (magasin) avec surbrillance optionnelle"""
    x, y = store_positions[i]
    
    # Choisir la couleur selon si le store a été modifié
    color = MODIFIED_COLOR if is_modified else WOOD
    border_width = 5 if is_modified else 3
    
    pygame.draw.rect(screen, color, (x-30, y-110, 60, 220))
    pygame.draw.rect(screen, BLACK, (x-30, y-110, 60, 220), border_width)
    
    # Compteur
    store_name = 'Store1' if i == 0 else 'Store2'
    count = game.state.board[store_name]
    
    font = pygame.font.SysFont(None, 48, bold=True)
    text = font.render(str(count), True, WHITE)
    screen.blit(text, (x - text.get_width()//2, y - text.get_height()//2))
    
    # Label
    label_font = pygame.font.SysFont(None, 20)
    player_label = "P1" if i == 0 else "P2"
    label = label_font.render(player_label, True, BLACK)
    screen.blit(label, (x - label.get_width()//2, y + 120))


def draw_menu():
    """Dessine le menu de choix du côté"""
    screen.fill((205, 170, 125))
    
    # Titre
    title_font = pygame.font.SysFont(None, 72, bold=True)
    title = title_font.render("MANCALA", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    # Question
    question_font = pygame.font.SysFont(None, 40, bold=True)
    question = question_font.render("Choisissez votre côté :", True, BLACK)
    screen.blit(question, (WIDTH//2 - question.get_width()//2, 180))
    
    # Bouton En bas (A-F)
    button_font = pygame.font.SysFont(None, 36)
    bottom_color = (0, 150, 255) if human_side_choice == "bottom" else (150, 150, 150)
    pygame.draw.rect(screen, bottom_color, (225, 260, 200, 70), border_radius=10)
    pygame.draw.rect(screen, BLACK, (225, 260, 200, 70), 4, border_radius=10)
    bottom_text = button_font.render("En bas", True, WHITE)
    screen.blit(bottom_text, (225 + 100 - bottom_text.get_width()//2, 275))
    af_text = pygame.font.SysFont(None, 28).render("(pits A-F)", True, WHITE)
    screen.blit(af_text, (225 + 100 - af_text.get_width()//2, 305))
    
    # Bouton En haut (G-L)
    top_color = (255, 100, 0) if human_side_choice == "top" else (150, 150, 150)
    pygame.draw.rect(screen, top_color, (475, 260, 200, 70), border_radius=10)
    pygame.draw.rect(screen, BLACK, (475, 260, 200, 70), 4, border_radius=10)
    top_text = button_font.render("En haut", True, WHITE)
    screen.blit(top_text, (475 + 100 - top_text.get_width()//2, 275))
    gl_text = pygame.font.SysFont(None, 28).render("(pits G-L)", True, WHITE)
    screen.blit(gl_text, (475 + 100 - gl_text.get_width()//2, 305))


def handle_menu_click(pos):
    """Gère les clics dans le menu"""
    global game_started, game, play, current_player, human_side_choice
    
    x, y = pos
    
    # Clic sur "En bas (A-F)"
    if 225 <= x <= 425 and 260 <= y <= 330:
        human_side_choice = "bottom"
        # Initialiser le jeu : Humain = Player 1 (bas), Ordinateur = Player 2 (haut)
        game = Game(humanPlayer=1, computerPlayer=2)
        play = Play(game)
        current_player = "HUMAN"  # L'humain commence toujours
        game_started = True
    
    # Clic sur "En haut (G-L)"
    elif 475 <= x <= 675 and 260 <= y <= 330:
        human_side_choice = "top"
        # Initialiser le jeu : Humain = Player 2 (haut), Ordinateur = Player 1 (bas)
        game = Game(humanPlayer=2, computerPlayer=1)
        play = Play(game)
        current_player = "HUMAN"  # L'humain commence toujours
        game_started = True


def draw_game_state():
    """Dessine tout le plateau de jeu"""
    screen.fill((205, 170, 125))
    
    # Vérifier si on doit encore afficher les surbrillances
    current_time = pygame.time.get_ticks()
    show_highlights = (current_time - highlight_start_time) < HIGHLIGHT_DURATION
    
    # Stores avec surbrillance si modifiés
    store1_modified = show_highlights and 'Store1' in modified_pits
    store2_modified = show_highlights and 'Store2' in modified_pits
    draw_store(0, store1_modified)
    draw_store(1, store2_modified)
    
    # Pits avec surbrillance
    for i in range(12):
        pit_letter = index_to_pit[i]
        pos = pit_positions[i]
        
        # Déterminer le type de surbrillance
        highlight = None
        if show_highlights:
            if pit_letter == highlighted_pit:
                highlight = "selected"
            elif pit_letter in modified_pits:
                highlight = "modified"
        
        draw_pit(pos, pit_letter, highlight)
        draw_seeds(game.state.board[pit_letter], pos[0], pos[1])
    
    # Afficher le tour actuel
    font = pygame.font.SysFont(None, 36, bold=True)
    if current_player == "HUMAN" and not delay_after_human_move:
        text = font.render("Votre tour (Player 1)" if game.playerSide["HUMAN"] == 1 else "Votre tour (Player 2)", True, (0, 100, 0))
    else:
        text = font.render("Tour de l'ordinateur (Player 2)" if game.playerSide["COMPUTER"] == 2 else "Tour de l'ordinateur (Player 1)", True, (200, 0, 0))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 10))
    
    # Afficher les infos du dernier coup de l'ordinateur
    if last_computer_move["pit"]:
        info_font = pygame.font.SysFont(None, 28)
        pit_text = info_font.render(
            f"Ordinateur a joué: {last_computer_move['pit']}", 
            True, 
            (200, 0, 0)
        )
        screen.blit(pit_text, (10, 50))
    
    # Légende des couleurs
    legend_font = pygame.font.SysFont(None, 20)
    pygame.draw.circle(screen, SELECTED_COLOR, (20, 370), 10)
    legend1 = legend_font.render("= Pit sélectionné", True, BLACK)
    screen.blit(legend1, (35, 363))
    
    pygame.draw.circle(screen, MODIFIED_COLOR, (200, 370), 10)
    legend2 = legend_font.render("= Pits/Stores modifiés", True, BLACK)
    screen.blit(legend2, (215, 363))
    
    # Afficher le gagnant si partie terminée
    if game.gameOver():
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        winner, score1, score2 = game.findWinner()
        result_font = pygame.font.SysFont(None, 64, bold=True)
        result_text = result_font.render(winner, True, (255, 215, 0))
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2 - 50))
        
        score_font = pygame.font.SysFont(None, 40)
        score_text = score_font.render(f"P1: {score1}  -  P2: {score2}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))


def get_clicked_pit(mouse_pos):
    """Retourne le pit cliqué (ou None)"""
    mx, my = mouse_pos
    
    for i in range(12):
        px, py = pit_positions[i]
        distance = math.sqrt((mx - px)**2 + (my - py)**2)
        
        if distance <= pit_radius:
            pit_letter = index_to_pit[i]
            return pit_letter
    
    return None


def detect_modified_pits(board_before, board_after):
    """Détecte quels pits ont été modifiés"""
    modified = set()
    for pit in board_before:
        if board_before[pit] != board_after[pit]:
            modified.add(pit)
    return modified


def computer_play():
    """Fait jouer l'ordinateur"""
    global last_computer_move, highlighted_pit, modified_pits, highlight_start_time, board_before_move
    
    moves = game.state.possibleMoves(game.playerSide["COMPUTER"])
    if not moves:
        return
    
    # Sauvegarder l'état avant le coup
    board_before_move = game.state.board.copy()
    
    # Minimax pour choisir le meilleur coup
    value, pit = play.minimaxAlphaBeta(game, 1, depth=6, alpha=-math.inf, beta=math.inf)
    
    # Sauvegarder les infos du coup
    last_computer_move = {"pit": pit, "value": value}
    
    print(f"L'ordinateur choisit {pit} (valeur = {value})")
    
    # Activer la surbrillance
    highlighted_pit = pit
    highlight_start_time = pygame.time.get_ticks()
    
    # Jouer le coup
    game.state.doMove(game.playerSide["COMPUTER"], pit)
    
    # Détecter les pits modifiés
    modified_pits = detect_modified_pits(board_before_move, game.state.board)


# ==================== BOUCLE PRINCIPALE ====================
running = True
clock = pygame.time.Clock()

while running:
    # Afficher le menu ou le jeu
    if not game_started:
        draw_menu()
    else:
        draw_game_state()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Clic de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si on est dans le menu
            if not game_started:
                handle_menu_click(event.pos)
            
            # Si on est dans le jeu
            elif not game.gameOver():
                # Si c'est le tour de l'humain (et pas en délai)
                if current_player == "HUMAN" and not delay_after_human_move:
                    clicked_pit = get_clicked_pit(event.pos)
                    
                    if clicked_pit:
                        # Vérifier que c'est un pit valide pour le joueur
                        moves = game.state.possibleMoves(game.playerSide["HUMAN"])
                        
                        if clicked_pit in moves:
                            print(f"Vous jouez : {clicked_pit}")
                            
                            # Sauvegarder l'état avant le coup
                            board_before_move = game.state.board.copy()
                            
                            # Activer la surbrillance
                            highlighted_pit = clicked_pit
                            highlight_start_time = pygame.time.get_ticks()
                            
                            # Jouer le coup
                            game.state.doMove(game.playerSide["HUMAN"], clicked_pit)
                            
                            # Détecter les pits modifiés
                            modified_pits = detect_modified_pits(board_before_move, game.state.board)
                            
                            # Activer le délai avant le tour de l'ordinateur
                            delay_after_human_move = True
                            delay_start_time = pygame.time.get_ticks()
                        else:
                            print(f"Pit invalide : {clicked_pit}")
    
    # Gérer le délai après le coup humain (seulement si le jeu a commencé)
    if game_started and delay_after_human_move:
        current_time = pygame.time.get_ticks()
        if (current_time - delay_start_time) >= DELAY_DURATION:
            delay_after_human_move = False
            current_player = "COMPUTER"
    
    # Tour de l'ordinateur (seulement si le jeu a commencé)
    if game_started and current_player == "COMPUTER" and not game.gameOver():
        pygame.time.wait(500)
        computer_play()
        current_player = "HUMAN"
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()