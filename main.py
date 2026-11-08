import math
import pygame
import pymunk

pygame.init()

# CONSTANTS
WIDTH, HEIGHT = 2000, 1200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BALL_RADIUS = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BALLS')
CLOCK = pygame.time.Clock()

# SKIP ICON IF NOT FOUND
try:
    pygame.display.set_icon(pygame.image.load('icon.png'))
except (FileNotFoundError, pygame.error):
    print('ICON SKIPPED, icon.png not found!')

# FONT (USING DEFAULT FONT IF text.ttf NOT FOUND)
try:
    font = pygame.font.Font('text.ttf', 24)
except (FileNotFoundError, OSError):
    print('text.ttf not found, forced to use default font!')
    font = pygame.font.Font(None, 28)

text = font.render('click to spawn a BALLS, click a BALL to delete it, use left click if you want to spam BALLS, press c to remove all the BALLS', True, WHITE)
textRect = text.get_rect(center=(WIDTH // 2, 30))

# PHYSICS SPACE
SPACE = pymunk.Space()
SPACE.gravity = (0, 1000)

# BORDER
top_left = (0, 0)
top_right = (WIDTH, 0)
bottom_left = (0, HEIGHT)
bottom_right = (WIDTH, HEIGHT)

for a, b in [
    (top_left, top_right),
    (top_left, bottom_left),
    (top_right, bottom_right),
    (bottom_left, bottom_right),
]:
    border = pymunk.Segment(SPACE.static_body, a, b, 2)
    border.elasticity = 1
    SPACE.add(border)

# BALLS
balls = []

# FUNCTIONS
# SPAWN BALLS
def spawn_ball(pos):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BALL_RADIUS))
    body.position = pos
    shape = pymunk.Circle(body, BALL_RADIUS)
    shape.elasticity = 0.8
    SPACE.add(body, shape)
    balls.append((body, shape))

# BALL POSITION
def ball_at(pos):
    for body, shape in reversed(balls):
        dx = body.position.x - pos[0]
        dy = body.position.y - pos[1]
        if math.hypot(dx, dy) <= BALL_RADIUS:
            return body, shape
    return None

# REMOVE BALLS
def remove_ball(ball):
    body, shape = ball
    SPACE.remove(body, shape)
    balls.remove(ball)
# CLEAR BALLS
def clear_balls():
    for body, shape in balls:
        SPACE.remove(body, shape)
    balls.clear()
# MAIN LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = ball_at(event.pos)
                if clicked:
                    remove_ball(clicked)
                else:
                    spawn_ball(event.pos)
            elif event.button == 3:
                spawn_ball(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                clear_balls()

    # PHYSICS
    SPACE.step(1 / 60.0)

    # DRAW
    WINDOW.fill(BLACK)
    WINDOW.blit(text, textRect)
    for body, shape in balls:
        pygame.draw.circle(
            WINDOW, GREEN,
            (int(body.position.x), int(body.position.y)),
            BALL_RADIUS
        )

    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()