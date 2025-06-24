import pygame
import math
import numpy as np
import sys

# Init
pygame.init()
WIDTH, HEIGHT = 320, 180
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
clock = pygame.time.Clock()

# Load and scale the track texture for better horizontal space
track = pygame.image.load("track.png").convert()
track = pygame.transform.scale(track, (1024, 1024))
track_width, track_height = track.get_size()

# Camera state
cam_x, cam_y = 300, 300  # center of image
cam_angle = 0.0
move_speed = 4.0
turn_speed = 2.5

# Optimized ray table (precalculate for all pixels)
ray_dx = np.array([x - WIDTH // 2 for x in range(WIDTH)])
sin_a = np.sin(np.radians(cam_angle))
cos_a = np.cos(np.radians(cam_angle))


def handle_input():
    global cam_x, cam_y, cam_angle, sin_a, cos_a
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        cam_x += cos_a * move_speed
        cam_y += sin_a * move_speed
    if keys[pygame.K_s]:
        cam_x -= cos_a * move_speed
        cam_y -= sin_a * move_speed
    if keys[pygame.K_a]:
        cam_angle -= turn_speed
    if keys[pygame.K_d]:
        cam_angle += turn_speed

    # Update trig values after changing cam_angle
    sin_a = np.sin(np.radians(cam_angle))
    cos_a = np.cos(np.radians(cam_angle))


def draw_floor():
    surface = pygame.surfarray.pixels3d(screen)
    horizon = int(HEIGHT * 0.2)
    fov = 500  # increase for more zoom-out
    depth = np.zeros(WIDTH, dtype=np.float32)

    for y in range(horizon, HEIGHT):
        depth[:] = fov / (y - horizon + 0.001)

        # Efficient vectorized computation for all pixels at once
        offset = ray_dx * depth / 100
        world_x = cam_x + (cos_a * depth) - (sin_a * offset)
        world_y = cam_y + (sin_a * depth) + (cos_a * offset)

        # Wrap around texture coordinates
        tx = (world_x.astype(int)) % track_width
        ty = (world_y.astype(int)) % track_height

        # Retrieve pixel colors for all x in one go (using vectorized access)
        for x in range(WIDTH):
            color = track.get_at((tx[x], ty[x]))[
                :3
            ]  # Access each tx, ty pair as tuples
            surface[x, y] = color


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
