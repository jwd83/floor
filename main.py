import pygame
import math
import numpy as np
import sys

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load track
track = pygame.image.load("track.png").convert()
track_width, track_height = track.get_size()

# Camera
cam_x, cam_y = 400, 300
cam_angle = 0
speed = 4
turn = 2

# Precompute x-ray directions
screen_half = WIDTH // 2
ray_table = np.array([x - screen_half for x in range(WIDTH)])

def handle_input():
    global cam_x, cam_y, cam_angle
    keys = pygame.key.get_pressed()
    rad = math.radians(cam_angle)
    if keys[pygame.K_w]:
        cam_x += math.cos(rad) * speed
        cam_y += math.sin(rad) * speed
    if keys[pygame.K_s]:
        cam_x -= math.cos(rad) * speed
        cam_y -= math.sin(rad) * speed
    if keys[pygame.K_a]:
        cam_angle -= turn
    if keys[pygame.K_d]:
        cam_angle += turn

def draw_floor():
    # Direct pixel access
    surface = pygame.surfarray.pixels3d(screen)
    horizon = HEIGHT // 2
    fov = 200  # controls field of view scale

    for y in range(horizon, HEIGHT):
        perspective = fov / (y - horizon + 1e-5)
        sin_a = math.sin(math.radians(cam_angle))
        cos_a = math.cos(math.radians(cam_angle))

        for x in range(WIDTH):
            dx = ray_table[x] * perspective
            world_x = cam_x + cos_a * perspective - sin_a * dx
            world_y = cam_y + sin_a * perspective + cos_a * dx

            tx = int(world_x) % track_width
            ty = int(world_y) % track_height

            surface[x, y] = track.get_at((tx, ty))[:3]

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        handle_input()
        screen.fill((50, 50, 50))  # optional: gray horizon
        draw_floor()
        pygame.display.flip()
        clock.tick(60)

main()
