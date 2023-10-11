import pygame
import random
from scipy.spatial import Voronoi
import numpy as np
from perlin import Perlin
import math

pygame.init()

"""settings"""
n_dots = 200
background_color = (39, 40, 41)
dots_color = (255, 246, 224)
polygon_color = (255, 246, 224)

"""display part"""
display_width = 1920
display_height = 1080

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Polygon")

"""fps part"""
clock = pygame.time.Clock()
FPS = 60


def crate_dots():
    dots = []
    for i in range(n_dots):
        rand_pos = (random.uniform(-50, display_width + 50), random.uniform(-50, display_height + 50))
        color = dots_color
        radius = 5
        dots.append(Dot(rand_pos, color, radius))
    return dots


def create_direction():
    v = np.random.rand(2)
    normalized_v = v / np.sqrt(np.sum(v ** 2))
    return normalized_v


def draw_polygons(dots):
    vor = Voronoi([dot.position for dot in dots], incremental=True)
    pol_edges = vor.vertices
    regions = vor.regions

    for region in regions:

        points = []
        for i in range(len(region)):
            if region[i] != -1:
                points.append(pol_edges[region[i]])

        if len(points) > 2:
            pygame.draw.polygon(display, polygon_color, points, 5)


class Dot:
    def __init__(self, position, color, radius):
        self.position = position
        self.color = color
        self.radius = radius
        self.direction = (np.random.rand(2) - 0.5)
        self.noise = Perlin(6789)

    def update(self, surf):
        
        self.position += self.direction

        # sometimes rotate direction vector
        if random.random() > 0.8:
            self.rotate_direction()

        # deflect direction vector from edges of field
        if self.position[0] < -50:
            self.position[0] = -50
            self.direction[0] *= -1
        if self.position[0] > display_width + 50:
            self.position[0] = display_width + 50
            self.direction[0] *= -1
        if self.position[1] < -50:
            self.position[1] = -50
            self.direction[1] *= -1
        if self.position[1] > display_height + 50:
            self.position[1] = display_height + 50
            self.direction[1] *= -1

        # pygame.draw.circle(surf, self.color, self.position, self.radius)

    def rotate_direction(self):
        """slightly rotate direction vector based on perlin noise"""
        rand_angle = self.noise.one(pygame.time.get_ticks()) / 100
        x = self.direction[0] * math.cos(rand_angle) - self.direction[1] * math.sin(rand_angle)
        y = self.direction[0] * math.sin(rand_angle) + self.direction[1] * math.cos(rand_angle)

        self.direction = [round(x, 2), round(y, 2)]


def main():
    in_game = True

    dots = crate_dots()

    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False

        display.fill(background_color)

        for dot in dots:
            dot.update(display)

        draw_polygons(dots)

        """display update"""
        clock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()




