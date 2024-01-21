import pygame

from paddle import Paddle


class Ball():
    color = (50, 40, 255)

    def __init__(self, paddle: Paddle, screen: pygame.Surface, speed: int):
        self.ballX = int(screen.get_width()/2)
        self.ballY = int(screen.get_height()*0.8)
        self.x_vel = speed
        self.y_vel = -speed
        self.ball_radius = 10
        self.max_x_vel = speed
        self.paddle = paddle
        self.screen = screen

    def show(self):
        pygame.draw.circle(self.screen, self.color,
                           (self.ballX, self.ballY), self.ball_radius)

    def move(self):
        self.ballX += self.x_vel
        self.ballY += self.y_vel

    def collision_change(self):
        center = self.paddle.paddleX + self.paddle.length/2
        left_end = self.paddle.paddleX
        right_end = self.paddle.paddleX + self.paddle.length
        self.y_vel = -self.y_vel
        if left_end < self.ballX < center:
            ratio = (center - self.ballX)/(self.paddle.length/2)
            self.x_vel += -self.max_x_vel * ratio
        elif center < self.ballX < right_end:
            ratio = (self.ballX - center)/(self.paddle.length/2)
            self.x_vel += self.max_x_vel * ratio

    def boundries(self):
        if self.ballY <= (0 + self.ball_radius):
            self.y_vel = -self.y_vel
        if self.ballX <= (0 + self.ball_radius):
            self.x_vel = -self.x_vel
        if self.ballX >= (self.screen.get_width() - self.ball_radius):
            self.x_vel = -self.x_vel

    def limit_vel(self):
        if -self.max_x_vel > self.x_vel:
            self.x_vel = -self.max_x_vel
        elif self.x_vel > self.max_x_vel:
            self.x_vel = self.max_x_vel

    def update(self):
        self.move()
        self.boundries()
        self.limit_vel()
