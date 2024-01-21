import random
import pygame


class Level():

    brick_colors = [(200, 50, 80), (45, 80, 240), (46, 235, 70),
                    (150, 50, 180), (230, 170, 80), (60, 230, 220), (180, 210, 80)]

    def __init__(self, screen: pygame.Surface, baground_color: tuple):
        self.screen = screen
        self.rows = 7
        self.rows_bricks = 9
        self.length = int(screen.get_width()*0.8)//self.rows_bricks
        self.width = 40
        self.spacing = 4
        self.bricks = []
        self.random_color = []
        self.background_color = baground_color
        for i in range(10, self.rows*(self.width), self.width):
            for j in range(int(screen.get_width()*0.1), int(screen.get_width()*0.9 - self.length)+1, self.length):
                self.bricks.append([j, i])
                self.random_color.append(random.choice(self.brick_colors))
        self.bricks_with_colors = {}
        for i in range(10, self.rows*(self.width), self.width):
            row_color = random.choice(self.brick_colors)
            for j in range(int(screen.get_width()*0.1), int(screen.get_width()*0.9 - self.length)+1, self.length):
                brick_position = (j, i)  # Store as a tuple
                self.bricks_with_colors[brick_position] = row_color


    def show(self):
        # Change: Iterate through the dictionary and draw each brick with its stored color
        for brick_position, brick_color in self.bricks_with_colors.items():
            pygame.draw.rect(self.screen, brick_color, (
                brick_position, (self.length-self.spacing, self.width-self.spacing)))

    def remove(self, brick):
        # Change: Use tuple for brick position
        if brick in self.bricks_with_colors:
            del self.bricks_with_colors[brick]
