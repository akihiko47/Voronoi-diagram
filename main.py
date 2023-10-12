import pygame
import random
from scipy.spatial import Voronoi  # main algorithm for building Voronoi diagram
from Classes import Dot  # Get DOT class

pygame.init()

"""SETTINGS"""
n_dots = 200
background_color = (0, 0, 0)
dots_color = (255, 246, 224)

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

        points = []  # get list of vertices for each polygon
        for i in range(len(region)):
            if region[i] != -1:  # if polygon vertex not in infinity
                point = pol_edges[region[i]]
                points.append(point)

        if len(points) > 2:  # if there are more than 2 vertices

            """Get color value from polygon Y coordinate"""
            old_value = sum([p[1] for p in points]) / len(points)  # polygon Y value (mean from vertices)
            old_min = -50  # minimal possible Y
            old_max = display_height + 50  # maximum possible Y
            new_min = 0  # minimal color value that we need
            new_max = 120  # maximum color value that we need
            new_value = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

            """Restrict color value to range"""
            if new_value < 0:
                new_value = 0
            if new_value > new_max:
                new_value = new_max

            color = (200, new_value, 20)
            pygame.draw.polygon(display, color, points, 10)


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




