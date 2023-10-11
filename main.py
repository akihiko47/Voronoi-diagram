import pygame
import random
from scipy.spatial import Voronoi  # main algorithm for building Voronoi diagram
from Classes import Dot  # Get DOT class

pygame.init()

"""SETTINGS"""
n_dots = 200
background_color = (39, 40, 41)
dots_color = (255, 246, 224)
polygon_color = (255, 246, 224)

"""display part"""
display_width = 1920  # change this to your preferences
display_height = 1080  # change this to your preferences

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Polygon")

"""fps part"""
clock = pygame.time.Clock()
FPS = 60


def crate_dots():
    """
    create list of dots with defined position, color and radius
    """

    dots = []
    for i in range(n_dots):
        rand_pos = (random.uniform(-50, display_width + 50), random.uniform(-50, display_height + 50))
        color = dots_color
        radius = 5
        dots.append(Dot(rand_pos, color, radius))
    return dots


def draw_polygons(dots):
    """
    Main algorithm for building Voronoi diagram
    Get polygon vertices and draw polygons from them
    For more information read about scipy.spatial.voronoi
    """

    vor = Voronoi([dot.position for dot in dots], incremental=True)
    pol_edges = vor.vertices
    regions = vor.regions

    for region in regions:

        points = []  # get list of vertices for each vertices
        for i in range(len(region)):
            if region[i] != -1:  # if polygon vertex not in infinity
                points.append(pol_edges[region[i]])

        if len(points) > 2:  # if there are more than 2 vertices
            pygame.draw.polygon(display, polygon_color, points, 5)


def main():
    """
    Main loop
    """

    dots = crate_dots()

    in_game = True
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False

        display.fill(background_color)

        """update dots"""
        for dot in dots:
            dot.update(display)

        """draw polygons from dots"""
        draw_polygons(dots)

        """display update"""
        clock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()




