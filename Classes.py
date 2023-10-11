import numpy as np
from perlin import Perlin
import pygame
import random
import math


class Dot:
    def __init__(self, position, color, radius):
        self.position = position
        self.color = color
        self.radius = radius
        self.direction = (np.random.rand(2) - 0.5)
        self.noise = Perlin(6789)

    def update(self, surf):
        """
        update dot data and draw them (if needed)
        """

        self.position += self.direction

        """sometimes rotate direction vector"""
        if random.random() > 0.8:
            self.rotate_direction()

        """deflect direction vector from edges of field"""
        display_width, display_height = surf.get_size()
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

        """uncomment this to draw dots"""
        # pygame.draw.circle(surf, self.color, self.position, self.radius)

    def rotate_direction(self):
        """
        slightly rotate direction vector based on perlin noise
        """

        rand_angle = self.noise.one(pygame.time.get_ticks()) / 100
        x = self.direction[0] * math.cos(rand_angle) - self.direction[1] * math.sin(rand_angle)
        y = self.direction[0] * math.sin(rand_angle) + self.direction[1] * math.cos(rand_angle)

        self.direction = [round(x, 2), round(y, 2)]