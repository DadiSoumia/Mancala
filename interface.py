import pygame
pygame.init()

# Fenêtre
WIDTH, HEIGHT = 900, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mancala - Pygame")

# Couleurs
WOOD = (205, 155, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SEED_COLORS = [(255,0,0),(0,255,0),(0,0,255),(150,0,150)]

# --- CONFIG ---
pit_radius = 40
seed_radius = 8

# positions des 12 pits (centrés et bien alignés)
pit_positions = [
    (170 + i*110, 120) for i in range(6)
] + [
    (170 + i*110, 280) for i in range(6)
]

# magasins
store_positions = [(60, 200), (840, 200)]
store_counts = [0, 0]

# grains dans chaque pit (4 grains/pit)
pits = [[1,1,1,1] for _ in range(12)]

# bouton
button_rect = pygame.Rect(400, 10, 120, 40)


def draw_pit(center):
    x, y = center
    pygame.draw.circle(screen, WOOD, (x, y), pit_radius)
    pygame.draw.circle(screen, BLACK, (x, y), pit_radius, 3)


def draw_seeds(seed_list, cx, cy):
    if not seed_list:
        return

    # placer les grains autour du centre
    offset_positions = [
        (-12, -10), (12, -10),
        (-12, 10), (12, 10)
    ]

    for i, seed in enumerate(seed_list):
        dx, dy = offset_positions[i % len(offset_positions)]
        color = SEED_COLORS[i % len(SEED_COLORS)]
        pygame.draw.circle(screen, color, (cx + dx, cy + dy), seed_radius)


def draw_store(i):
    x, y = store_positions[i]
    pygame.draw.rect(screen, WOOD, (x-25, y-110, 50, 220))
    pygame.draw.rect(screen, BLACK, (x-25, y-110, 50, 220), 3)

    # texte compteur
    font = pygame.font.SysFont(None, 36)
    text = font.render(str(store_counts[i]), True, WHITE)
    screen.blit(text, (x - text.get_width()//2, y - 20))


def draw_button():
    pygame.draw.rect(screen, (0, 150, 250), button_rect)
    font = pygame.font.SysFont(None, 30)
    txt = font.render("Jouer", True, WHITE)
    screen.blit(txt, (button_rect.x + 20, button_rect.y + 7))


running = True
while running:
    screen.fill((205, 170, 125))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # bouton cliqué
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Bouton JOUER cliqué")
                # ➡➡ ici tu mets ta logique du jeu ❤️

    # dessiner les magasins
    for i in range(2):
        draw_store(i)

    # dessiner pits + grains
    for i, pos in enumerate(pit_positions):
        draw_pit(pos)
        draw_seeds(pits[i], pos[0], pos[1])

    # bouton
    draw_button()

    pygame.display.update()

pygame.quit()
