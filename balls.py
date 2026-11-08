import pygame
import pymunk

pygame.init()

# CONSTANTS
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
SPACE = pymunk.Space()
SPACE.gravity = (0, 1000)
ICON = pygame.image.load('icon.png')
BALL_RADIUS = 20

top_left = (0, 0)
top_right = (WIDTH, 0)
bottom_left = (0, HEIGHT)
bottom_right = (WIDTH, HEIGHT)

pygame.display.set_caption('BALLS')
pygame.display.set_icon(ICON)

# BORDER
for border in [
    pymunk.Segment(SPACE.static_body, top_left, top_right, 2),
    pymunk.Segment(SPACE.static_body, top_left, bottom_left, 2),
    pymunk.Segment(SPACE.static_body, top_right, bottom_right, 2),
    pymunk.Segment(SPACE.static_body, bottom_left, bottom_right, 2),
]:
    border.elasticity = 1
    SPACE.add(border)

# BALLS
balls = []

#CLICK BALL
def spawn_ball(pos):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BALL_RADIUS))
    body.position = pos
    shape = pymunk.Circle(body, BALL_RADIUS)
    shape.elasticity = 0.8
    SPACE.add(body, shape)
    balls.append((body, shape))


def ball_at(pos):
    mouse = pymunk.Vec2d(*pos)
    for body, shape in reversed(balls):
        if body.position.get_distance(mouse) <= BALL_RADIUS:
            return body, shape
    return None

#REMOVE BALL CLICK
def remove_ball(ball):
    body, shape = ball
    SPACE.remove(body, shape)
    balls.remove(ball)


# LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = ball_at(event.pos)
            if clicked:
                remove_ball(clicked)
            else:
                spawn_ball(event.pos)

    # PHYSICS
    SPACE.step(1 / 60.0)

    # DRAW
    WINDOW.fill((0, 0, 0))
    for body, shape in balls:
        pygame.draw.circle(
            WINDOW, (0, 255, 0),
            (int(body.position.x), int(body.position.y)),
            BALL_RADIUS
        )

    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()