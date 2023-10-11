import pygame
import random
from scipy.spatial import Voronoi
import numpy as np

pygame.init()

"""settings"""
n_dots = 100
background_color = (173, 196, 206)
dots_color = (241, 240, 232)
polygon_color = (241, 240, 232)

"""display part"""
display_width = 1280
display_height = 720

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Polygon")

"""fps part"""
clock = pygame.time.Clock()
FPS = 60

dots = np.array([(random.randint(-100, display_width+100), random.randint(-100, display_height+100)) for _ in range(n_dots)])


def main():
    in_game = True

    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False

        display.fill(background_color)

        for dot in dots:
            pygame.draw.circle(display, dots_color, dot, 5)

        vor = Voronoi(dots, qhull_options='Qbb Qc Qx')
        pol_edges = vor.vertices
        regions = vor.regions

        for region in regions:

            points = []

            for i in range(-1, len(region)):
                if region[i] != -1:
                    points.append(pol_edges[region[i]])

            pygame.draw.polygon(display, polygon_color, points, 5)


        """display update"""
        clock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()




