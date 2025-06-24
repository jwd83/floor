import pygame
import math
import numpy as np
import sys

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load and scale the track texture for better horizontal space
track = pygame.image.load("track.png").convert()
track = pygame.transform.scale(track, (1024, 1024))
track_width, track_height = track.get_size()

# Camera state
cam_x, cam_y = 512, 512  # center of image
cam_angle = 0.0
move_speed = 4.0
turn_speed = 2.5

# Optimized ray table
ray_dx = np.array([x - WIDTH // 2 for x in range(WIDTH)])


def handle_input():
    global cam_x, cam_y, cam_angle
    keys = pygame.key.get_pressed()
    rad = math.radians(cam_angle)

    if keys[pygame.K_w]:
        cam_x += math.cos(rad) * move_speed
        cam_y += math.sin(rad) * move_speed
    if keys[pygame.K_s]:
        cam_x -= math.cos(rad) * move_speed
        cam_y -= math.sin(rad) * move_speed
    if keys[pygame.K_a]:
        cam_angle -= turn_speed
    if keys[pygame.K_d]:
        cam_angle += turn_speed


def draw_floor():
    surface = pygame.surfarray.pixels3d(screen)
    horizon = HEIGHT // 2
    fov = 300  # increase for more zoom-out

    cos_a = math.cos(math.radians(cam_angle))
    sin_a = math.sin(math.radians(cam_angle))

    for y in range(horizon, HEIGHT):
        depth = fov / (y - horizon + 0.001)

        for x in range(WIDTH):
            offset = ray_dx[x]
            world_x = cam_x + (cos_a * depth) - (sin_a * offset * depth / 100)
            world_y = cam_y + (sin_a * depth) + (cos_a * offset * depth / 100)

            # Wrap around
            tx = int(world_x) % track_width
            ty = int(world_y) % track_height
            surface[x, y] = track.get_at((tx, ty))[:3]


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        handle_input()
        screen.fill((135, 206, 235))  # sky blue top half
        draw_floor()
        pygame.display.flip()
        clock.tick(60)


main()
