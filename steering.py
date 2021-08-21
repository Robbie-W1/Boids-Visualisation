from animation import Animation
import pygame.gfxdraw
from math import sin, cos, atan2, pi, sqrt
from vectors import Vector


class Target:

    def __init__(self, window):
        self.position = Vector(0, 0)
        self.radius = 20
        self.window = window
        self.color = (0, 200, 0)

    def update(self, mouse_x, mouse_y):
        self.position.x = mouse_x
        self.position.y = mouse_y

    def draw(self):
        pygame.gfxdraw.filled_circle(
            self.window.screen, self.position.x, self.position.y, self.radius, self.color)


class Seeker:

    def __init__(self, window):
        self.window = window
        self.position = Vector(self.window.width // 2, self.window.height // 2)
        self.velocity = Vector(2, -1)
        self.calculate_heading()
        self.color = (255, 255, 255)
        self.length = 30
        self.width = 20
        self.max_speed = 2
        self.max_force = 2
        self.acceleration = Vector(0, 0)

    def calculate_heading(self):
        self.heading = atan2(self.velocity.x, self.velocity.y)

    def seek(self, target):
        force = target.position - self.position
        force_magnitude = sqrt(force.x ** 2 + force.y ** 2)

        # set the magnitude of the force to the max speed
        force = force * (self.max_force / force_magnitude)
        self.acceleration += force

    def update(self):
        self.velocity += self.acceleration

        speed = sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)
        if speed > self.max_speed:
            speed * (self.max_speed / speed)

        self.position += self.velocity

        self.calculate_heading()
        self.calculate_points()

        print(
            f"Acceleration = {self.acceleration},\t Velocity = {self.velocity}")
        self.acceleration.x, self.acceleration.y, = 0, 0

    def calculate_points(self):
        self.front_x = int(
            self.position.x + ((self.length) * sin(self.heading)))
        self.front_y = int(
            self.position.y + ((self.length) * cos(self.heading)))

        self.back_left_x = int(
            self.position.x + ((self.width/2) * sin(self.heading+(pi/2))))
        self.back_left_y = int(
            self.position.y + ((self.width/2) * cos(self.heading+(pi/2))))

        self.back_right_x = int(
            self.position.x - ((self.width/2) * sin(self.heading+(pi/2))))
        self.back_right_y = int(
            self.position.y - ((self.width/2) * cos(self.heading+(pi/2))))

    def draw(self):
        pygame.gfxdraw.filled_trigon(self.window.screen,
                                     self.front_x, self.front_y,
                                     self.back_left_x, self.back_left_y,
                                     self.back_right_x, self.back_right_y,
                                     (255, 255, 255))


def main():
    window = Animation(800, 600, color=(50, 50, 50))
    target = Target(window)
    seeker = Seeker(window)

    while True:
        window.check_quit()
        window.clear()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        target.update(mouse_x, mouse_y)
        seeker.seek(target)
        seeker.update()
        target.draw()
        seeker.draw()
        window.draw()


if __name__ == '__main__':
    main()
