import pygame


class Paddle():
    paddle_color = (80, 50, 30)

    def __init__(self, screen: pygame.Surface):
        self.paddleX = int(screen.get_width()*0.45)
        self.paddleY = int(screen.get_height()*0.95)
        self.length = 120
        self.screen = screen

    def show(self):
        thickness = 10
        pygame.draw.rect(self.screen, self.paddle_color, ((
            self.paddleX, self.paddleY), (self.length, thickness)))

    def move_left(self):
        self.velocity = 15
        self.paddleX += -self.velocity

    def move_right(self):
        self.velocity = 15
        self.paddleX += self.velocity

    def auto_left(self):
        self.velocity = 30
        self.paddleX += -self.velocity

    def auto_right(self):
        self.velocity = 30
        self.paddleX += self.velocity

    def stop(self):
        self.velocity = 0

    def boundries(self):
        if self.paddleX >= (self.screen.get_width() - self.length):
            self.paddleX = self.screen.get_width() - self.length
        elif self.paddleX <= 0:
            self.paddleX = 0
