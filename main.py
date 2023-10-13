import pygame
import random
from scipy.spatial import Voronoi  # main algorithm for building Voronoi diagram
from Classes import Dot  # Get DOT class

pygame.init()

"""SETTINGS"""
n_dots = 150
background_color = (0, 8, 8)
dots_color = (255, 246, 224)  # uncomment draw line in Dot class (Classes.py)

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


def draw_lines(dots):
    """
    Main algorithm for building Voronoi diagram
    Get polygon vertices and draw lines from them
    For more information read about scipy.spatial.voronoi
    """

    vor = Voronoi([dot.position for dot in dots], incremental=True)
    pol_vertices = vor.vertices
    pol_lines_indices = vor.ridge_vertices

    for pnt1_index, pnt2_index in pol_lines_indices:
        if pnt1_index != -1 and pnt2_index != -1:
            pnt1_cords = pol_vertices[pnt1_index]
            pnt2_cords = pol_vertices[pnt2_index]

            """Get color value from line Y coordinate"""
            old_value = (pnt1_cords[1] + pnt2_cords[1]) / 2  # mean Y value of 2 dots
            old_min = -50  # minimal possible Y
            old_max = display_height + 50  # maximum possible Y
            new_min = 0  # minimal color value that we need
            new_max = 255  # maximum color value that we need
            new_value = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

            """Restrict color value to range"""
            if new_value < 0:
                new_value = 0
            if new_value > new_max:
                new_value = new_max

            """Create color to this line from its Y value"""
            color = (new_value, 200, 255 - new_value)

            """Draw line"""
            pygame.draw.line(display, color, pnt1_cords, pnt2_cords, 15)  # big line
            pygame.draw.line(display, background_color, pnt1_cords, pnt2_cords, 5)  # small line in middle

            pygame.draw.circle(display, color, pnt1_cords, 10)  # circle in connections
            pygame.draw.circle(display, color, pnt2_cords, 10)  # circle in connections


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

        """draw lines from dots"""
        draw_lines(dots)

        """display update"""
        clock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
